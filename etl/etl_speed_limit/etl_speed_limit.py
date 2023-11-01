import json

import pandas as pd
import requests
from sqlalchemy import create_engine, inspect, text


def create_local_engine(db_user, db_password, db_host, db_name):
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )
    return engine


def get_lat_lon_df(engine):
    if not inspect(engine).has_table("routemodel"):
        raise SystemError("routemodel table does not exist in database")
    routemodel_df = pd.read_sql_query(
        sql="SELECT id, lat, lon FROM routemodel ORDER BY id ASC", con=engine
    )
    return routemodel_df


def get_streetname_speedlimits(lat_lon_df, BING_MAPS_API_KEY):
    # Create (lat, lon) "chunks" to send to API
    CHUNK_SIZE = 500  # Can't be >500
    coordinates = list(zip(lat_lon_df.lat, lat_lon_df.lon))
    coordinate_chunks = [
        coordinates[i : i + CHUNK_SIZE] for i in range(0, len(coordinates), CHUNK_SIZE)
    ]

    # Get lat, lon, street name, and speed limit from Bing API
    url = f"https://dev.virtualearth.net/REST/v1/Routes/SnapToRoad?key={BING_MAPS_API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "points": [],
        # "interpolate": True,  # Investigate what this does if have time
        "includeSpeedLimit": True,
        "speedUnit": "KPH",
    }
    lats = []
    lons = []
    street_names = []
    speed_limits = []
    for i, coordinate_chunk in enumerate(coordinate_chunks):
        print(
            f"Fetching {i*CHUNK_SIZE+1}-{min((i+1)*CHUNK_SIZE, len(coordinates))} of {len(coordinates)}"
        )
        body["points"] = [
            {"latitude": lat, "longitude": lon} for lat, lon in coordinate_chunk
        ]
        bing_maps_res = requests.post(
            url=url, headers=headers, data=json.dumps(body)
        ).json()
        resourceSets = bing_maps_res["resourceSets"]
        assert len(resourceSets) == 1
        assert len(resourceSets[0]["resources"]) == 1
        bing_maps_res = resourceSets[0]["resources"][0]["snappedPoints"]
        for data in bing_maps_res:
            lats.append(data["coordinate"]["latitude"])
            lons.append(data["coordinate"]["longitude"])
            street_names.append(data["name"])
            speed_limits.append(
                max(40, data["speedLimit"])
            )  # set speed limit at least 40km/h
        streetname_speedlimit_df = pd.DataFrame(
            {
                "lats": lats,
                "lons": lons,
                "street_names": street_names,
                "speed_limits": speed_limits,
            }
        )
    streetname_speedlimit_df.to_csv("./streetname_speedlimit.csv")
    return streetname_speedlimit_df


def find_closest_points(streetname_speedlimit_df, engine):
    # Find map Bing coors to our routemodel coors and return df
    query_values_data = str(
        list(
            zip(
                streetname_speedlimit_df.lats,
                streetname_speedlimit_df.lons,
                streetname_speedlimit_df.street_names,
                streetname_speedlimit_df.speed_limits,
            )
        )
    ).strip("[]")
    closest_points_query_string = f"""
    SELECT
        points.*,
        closest_point.*
    FROM (
        VALUES
            {query_values_data}
    ) AS points(lat, lon, street_name, speed_limit_km_per_h)
    CROSS JOIN LATERAL (
        SELECT
            id AS routemodel_id,
            lat AS routemodel_lat,
            lon AS routemodel_lon,
            ST_Distance(routemodel.geo , ST_SetSRID(ST_MakePoint(points.lon, points.lat), 4326)) AS distance
        FROM routemodel
        ORDER BY routemodel.geo <-> ST_SetSRID(ST_MakePoint(points.lon, points.lat), 4326)
        LIMIT 1
    ) AS closest_point;
    """
    closest_points_df = pd.read_sql_query(sql=closest_points_query_string, con=engine)
    closest_points_df.to_csv("./closest_points_df.csv")
    return closest_points_df


def add_stname_speedlimit_to_database(closest_points_df, engine):
    update_values_data = str(
        list(
            zip(
                closest_points_df.routemodel_id,
                closest_points_df.street_name,
                closest_points_df.speed_limit_km_per_h,
            )
        )
    ).strip("[]")
    closest_points_update_string = f"""
    UPDATE routemodel as r SET
        street_name = data.street_name,
        speed_limit_km_per_h = data.speed_limit_km_per_h
    FROM (VALUES
        {update_values_data} 
    ) AS data(id, street_name, speed_limit_km_per_h) 
    where r.id = data.id;
    """
    with engine.begin() as con:
        con.execute(
            text(closest_points_update_string).execution_options(autocommit=True)
        )


def main(db_user, db_password, db_host, db_name, BING_MAPS_API_KEY):
    print("1) Creating local database engine...")
    engine = create_local_engine(db_user, db_password, db_host, db_name)

    print("2) Getting lat, lon data from routemodel table...")
    lat_lon_df = get_lat_lon_df(engine)

    print("3) Fetching street names and speed limits for coordinates...")
    streetname_speedlimit_df = get_streetname_speedlimits(lat_lon_df, BING_MAPS_API_KEY)

    print("4) Mapping Bing data coordinates to routemodel coordinates...")
    closest_points_df = find_closest_points(streetname_speedlimit_df, engine)

    print("5) Adding street names and speed limits to database...")
    add_stname_speedlimit_to_database(closest_points_df, engine)


if __name__ == "__main__":
    db_user = ""
    db_password = ""
    db_host = ""
    db_name = ""
    BING_MAPS_API_KEY = ""
    main(db_user, db_password, db_host, db_name, BING_MAPS_API_KEY)
