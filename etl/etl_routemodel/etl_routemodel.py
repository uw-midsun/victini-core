import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from geoalchemy2 import Geometry
from geopy import distance
from sqlalchemy import create_engine, inspect, String
from collections import defaultdict
from sklearn.neighbors import BallTree


def geo_json_to_gpx_json(routes_filepath, routepoints_filepath, waypoints_filepath):
    routeDataGJ = []
    with open(routes_filepath, 'r') as f:
        routeDataGJ = json.load(f)

    routePointsGJ = []
    with open(routepoints_filepath, 'r') as f:
        routePointsGJ = json.load(f)
        routePointsGJ = routePointsGJ["features"]

    wayPointsGJ = []
    with open(waypoints_filepath, 'r') as f:
        wayPointsGJ = json.load(f)
        wayPointsGJ = wayPointsGJ['features']

    def flatten_route_points(rpGJ):
        routePoints = []
        for rp in rpGJ:
            routePoints.append(
                [
                    rp["properties"]["route_fid"],
                    rp["properties"]["route_point_id"],
                    rp["geometry"]["coordinates"][0],
                    rp["geometry"]["coordinates"][1],
                ]
            )
        return np.array(routePoints)
    
    allRPs = flatten_route_points(routePointsGJ)

    # Could be useful but not being used
    # def group_route_points(rpGJ):
    #     groupedRPs = {}
    #     currId = rpGJ[0]["properties"]["route_fid"]
    #     points = []
    #     for rp in rpGJ:
    #         fid = rp["properties"]["route_fid"]
    #         lng = rp["geometry"]["coordinates"][0]
    #         lat = rp["geometry"]["coordinates"][1]
    #         ele = rp["properties"]["ele"]

    #         if fid != currId:
    #             groupedRPs[currId] = points
    #             currId = fid
    #             points = []
    #         points.append([lng, lat, ele])

    #     return groupedRPs

    
    # groupedRPs = group_route_points(routePointsGJ)

    def assign_wps_to_routes(WPs, RPs):
        coordinates = RPs[:, -2:]
        routes = RPs[:, 0]
        groupedWPs = defaultdict(list)
        
        bt = BallTree(np.radians(coordinates), metric="haversine")
        for wp in WPs:
            lng = wp['geometry']['coordinates'][0]
            lat = wp['geometry']['coordinates'][1]
            # Increase k if a waypoint can be part of multiple routes, that is we can check the
            # k closest points to see which routes they belong to (k = 1 => closest route only)
            distances, indices = bt.query([np.radians([lng, lat])], k = 1)
            closestRoutes = set()
            for i in indices[0]:
                closestRoutes.add(routes[i])
            for r in closestRoutes:
                groupedWPs[int(r)].append(wp)

        return groupedWPs

    groupedWPs = assign_wps_to_routes(wayPointsGJ, allRPs)

    routesGJ = routeDataGJ['features']
    routesJ = []
    routeNames = []

    # Iterate over each route/loop
    for i, routeGJ in enumerate(routesGJ):
        name = routeGJ['properties']['name']
        routePointsGJ = routeGJ['geometry']['coordinates']
        start = routePointsGJ[0]
        end = routePointsGJ[-1]

        points = []
        prevP = None


        # Iterate over each point in the current route
        for p in routePointsGJ:

            # Loops over all waypoints assigned to the current route and determines if it should be inserted
            # at the current point
            def findAndAddWP(prevP = None, p = None):
                if not prevP:
                    return False

                # Determines if a wp is between p1 and p2 (wp is in the bounding box defined by p1 and p2)
                def isInBoundingBox(wp, p1, p2):
                    maxLng = max(p1[0], p2[0]) + 0.000045 # Might need to account for width of road in some cases?
                    minLng = min(p1[0], p2[0]) - 0.000045
                    maxLat = max(p1[1], p2[1]) + 0.000045
                    minLat = min(p1[1], p2[1]) - 0.000045

                    return wp[0] <= maxLng and wp[0] >= minLng and wp[1] <= maxLat and wp[1] >= minLat

                for wp in groupedWPs[i]:
                    lng = wp['geometry']['coordinates'][0]
                    lat = wp['geometry']['coordinates'][1]
                    if isInBoundingBox((lng, lat), prevP, p):
                        points.append({
                            'lng': wp['geometry']['coordinates'][0],
                            'lat': wp['geometry']['coordinates'][1],
                            "type": "waypoint"
                        })
                        points.append({
                            'lng': p[0], 
                            'lat': p[1]
                        })
                        groupedWPs[i].remove(wp)
                        return True
                
                return False

            if not findAndAddWP(prevP, p):
                points.append(
                    {
                        'lng': p[0], 
                        'lat': p[1]
                    }
                )
            prevP = p

        # If groupedWPs[i] is not empty, potentialy waypoints at the start and end of loop
        # They are not between existing route points so they would not be added in findAdnAddWP
        for wp in groupedWPs[i]:
            lng = wp['geometry']['coordinates'][0]
            lat = wp['geometry']['coordinates'][1]
            if distance.great_circle((lat, lng), (start[1], start[0])).m <= 50:
                points.insert(0, {
                    'lng': wp['geometry']['coordinates'][0],
                    'lat': wp['geometry']['coordinates'][1],
                    "type": "waypoint"
                })
            elif distance.great_circle((lat, lng), (end[1], end[0])).m <= 50:
                points.append({
                    'lng': wp['geometry']['coordinates'][0],
                    'lat': wp['geometry']['coordinates'][1],
                    "type": "waypoint"
                })
        
        route = {
            "mode": "driving",
            'points': points
        }

        routesJ.append(route)
        routeNames.append(name)

    return (routesJ, routeNames)


def gpx_json_to_gdf(json_filepath):
    file = Path(json_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")

    gdf_rows = []
    with open(json_filepath, "r") as f:
        gpx = json.load(f)
    for point in gpx["points"]:
        lon = point.get("lng", 0)
        lat = point.get("lat", None)
        data = {
            "lon": lon,
            "lat": lat,
            "geo": "POINT({} {})".format(lon, lat),
            "type": point.get("type", None),
            "street_name": None,
            "step": point.get("step", None),
            "next_turn": point.get("nextturn", None),
            "dir": None,
            "speed_limit_km_per_h": None,
            "gpx_dist_to_next_waypoint_m": None,
            "gpx_elapsed_dist_m": None,
            "geopy_elapsed_dist_m": 0,
            "geopy_dist_from_last_m": 0,
            "weather_id": None,
            # "time_to_next_s": None,
        }
        if dir := point.get("dir", None):
            soup = BeautifulSoup(dir, "html.parser")
            data["dir"] = soup.get_text()
        if dist := point.get("dist", None):
            data["gpx_dist_to_next_waypoint_m"] = dist["val"]
            data["gpx_elapsed_dist_m"] = dist["total"] - dist["val"]
        if len(gdf_rows) > 0:
            prev = gdf_rows[-1]
            prev_coor = (prev["lat"], prev["lon"])
            curr_coor = (data["lat"], data["lon"])
            dist = distance.great_circle(prev_coor, curr_coor).m
            data["geopy_dist_from_last_m"] = dist
            data["geopy_elapsed_dist_m"] = prev["geopy_elapsed_dist_m"] + dist
        # if time := point.get("timeto", None):
        #     data["time_to_next_s"] = time["val"]
        gdf_rows.append(data)

    gdf = gpd.GeoDataFrame(gdf_rows)
    csv_filepath = file.with_suffix(".csv")
    gdf.to_csv(csv_filepath)
    return csv_filepath


def seed_from_csv(csv_filepath, db_user, db_password, db_host, db_name):
    file = Path(csv_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")
    gdf = gpd.GeoDataFrame(pd.read_csv(file))
    gdf.fillna(np.nan).replace([np.nan], [None])
    gdf = gdf.drop(columns=["Unnamed: 0"])
    gdf.index.name = "id"
    # gdf = gdf.head(10) # For testing purposes

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    gdf.index += 1  # Making table 1-indexed
    if inspect(engine).has_table("routemodel"):
        row_len = pd.read_sql_query(sql="SELECT COUNT(*) FROM routemodel", con=engine)
        gdf.index += row_len.iloc[0, 0]

    response = gdf.to_sql(
        name="routemodel",
        con=engine,
        schema="public",
        if_exists="append",
        index=True,
        method="multi",
        dtype={"geo": Geometry("POINT", srid=4326), "street_name": String},
    )
    if gdf.shape[0] != response:
        raise SystemError("dataframe insertion failed")
    else:
        print("routemodel dataframe insertion success")


def main(gpx_json_filepath, db_user, db_password, db_host, db_name):
    print("1) Parsing gpx json format to csv format...")
    csv_filepath = gpx_json_to_gdf(gpx_json_filepath)

    print("2) Seeding routemodel csv into database...")
    seed_from_csv(csv_filepath, db_user, db_password, db_host, db_name)


if __name__ == "__main__":
    gpx_json_filepath = ""
    db_user = ""
    db_password = ""
    db_host = ""
    db_name = ""
    main(gpx_json_filepath, db_user, db_password, db_host, db_name)
