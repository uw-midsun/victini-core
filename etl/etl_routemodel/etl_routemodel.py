"""
etl_routemodel.py loads routemodel data into the database in two steps:
1. Creates data/routemodel.csv from a gpx file
2. Takes data/routemodel.csv and loads it into the Azure Postgres db
"""

# Step 1

import pandas as pd
import json
from bs4 import BeautifulSoup
from geopy import distance

# Bring the db_gateway models into scope
import sys, os
from os.path import dirname, abspath, join, normpath
sys.path.append(normpath(abspath(join(dirname(__file__), '..', '..'))))

print(sys.path)

def gpx_json_to_df(json_filepath):
    df_rows = []
    with open(json_filepath, "r") as f:
        gpx = json.load(f)
    for point in gpx["points"]:
        data = {
            "lon": point.get("lng", None),
            "lat": point.get("lat", None),
            "type": point.get("type", None),
            "step": point.get("step", None),
            "next_turn": point.get("nextturn", None),
            "dir": None,
            "gpx_dist_to_next_waypoint_m": None,
            "gpx_elapsed_dist_m": None,
            "geopy_elapsed_dist_m": 0,
            "geopy_dist_from_last_m": 0,
            # "time_to_next_s": None,
        }
        if dir := point.get("dir", None):
            soup = BeautifulSoup(dir, "html.parser")
            data["dir"] = soup.get_text()
        if dist := point.get("dist", None):
            data["gpx_dist_to_next_waypoint_m"] = dist["val"]
            data["gpx_elapsed_dist_m"] = dist["total"] - dist["val"]
        if len(df_rows) > 0:
            prev = df_rows[-1]
            prev_coor = (prev["lat"], prev["lon"])
            curr_coor = (data["lat"], data["lon"])
            dist = distance.great_circle(prev_coor, curr_coor).m
            data["geopy_dist_from_last_m"] = dist
            data["geopy_elapsed_dist_m"] = prev["geopy_elapsed_dist_m"] + dist
        # if time := point.get("timeto", None):
        #     data["time_to_next_s"] = time["val"]

        df_rows.append(data)
    return pd.DataFrame(df_rows)

# Step 2

# Import database information from db_gateway
# Note, it's important to import the Base instead of redeclaring, otherwise create_all() will fail
from db_gateway.src.database import Base, engine, db_session

def check_null(value):
    return None if pd.isnull(value) else value

def seed_from_csv(filename):
    # import all modules here that might define models before calling init_db()
    from db_gateway.src.models import RouteModel

    Base.metadata.create_all(bind=engine, tables=[RouteModel.__table__])

    df = pd.read_csv(filename)
    for row in df.itertuples():
        location = RouteModel(
            id=row.Index + 1,
            lat=check_null(row.lat),
            lon=check_null(row.lon),
            type=check_null(row.type),
            step=check_null(row.step),
            next_turn=check_null(row.next_turn),
            dir=check_null(row.dir),
            gpx_dist_to_next_waypoint_m=check_null(row.gpx_dist_to_next_waypoint_m),
            gpx_elapsed_dist_m=check_null(row.gpx_elapsed_dist_m),
            geopy_elapsed_dist_m=check_null(row.geopy_elapsed_dist_m),
            geopy_dist_from_last_m=check_null(row.geopy_dist_from_last_m),
        )
        db_session.add(location)
    db_session.commit()


if __name__ == "__main__":
    route_model_json_filepath = normpath(abspath(join(dirname(__file__), '..', 'data', 'routemodel_gpx.json'))) 
    route_model_csv_filepath = normpath(abspath(join(dirname(__file__), '..', 'data', 'routemodel_gpx.csv'))) 

    print(route_model_json_filepath, route_model_csv_filepath)

    if not os.path.exists(route_model_csv_filepath):
        df = gpx_json_to_df(route_model_json_filepath)
        df.to_csv(route_model_csv_filepath)
    seed_from_csv(route_model_csv_filepath)
    print("Success!")