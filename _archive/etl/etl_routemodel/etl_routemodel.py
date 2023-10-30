"""
etl_routemodel.py loads routemodel data into the database in two steps:
1. Creates data/routemodel.csv from a gpx file
2. Takes data/routemodel.csv and loads it into the Azure Postgres db

Here is a suggested route: https://www.google.ca/maps/dir/Fulton,+MO,+USA/Davenport/Great+River+Rd+%26+Gaylord+Nelson+Hwy,+Trenton,+WI+54014,+USA/@42.7215958,-91.0372306,7z/data=!3m1!4b1!4m35!4m34!1m5!1m1!1s0x87dc8e579b700d25:0xf0215f3f96f20e66!2m2!1d-91.9479586!2d38.8467082!1m20!1m1!1s0x87e234c5e012a2f1:0xe8ea1f6356581fb0!2m2!1d-90.5776367!2d41.5236437!3m4!1m2!1d-92.2319476!2d44.4238558!3s0x87f8338724908edf:0xca9b25d292ef7845!3m4!1m2!1d-92.3766828!2d44.5058247!3s0x87f82f351959945f:0x50b0245a3e723deb!3m4!1m2!1d-92.4467661!2d44.544585!3s0x87f827936d27e451:0xb48e8cc83edcbde7!1m5!1m1!1s0x87f78be36d3d1e0b:0x177144dc524ef09d!2m2!1d-92.5279297!2d44.6013121!3e0?entry=ttu
Route is 535 miles along the Mississippi River from Fulton, MO to Trenton, WI :)
"""

# Step 1

import pandas as pd
import json
from bs4 import BeautifulSoup
from geopy import distance

# Bring the db_gateway models into scope
import sys, os
from os.path import dirname, abspath, join, normpath

sys.path.append(normpath(abspath(join(dirname(__file__), "..", ".."))))


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
            "weather_id": None,
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
    from db_gateway.src.models import RouteModel, Weather

    Base.metadata.create_all(
        bind=engine, tables=[RouteModel.__table__, Weather.__table__]
    )

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
            weather_id=None,
        )
        db_session.add(location)
    db_session.commit()


if __name__ == "__main__":
    route_model_json_filepath = normpath(
        abspath(join(dirname(__file__), "..", "data", "routemodel_gpx.json"))
    )
    route_model_csv_filepath = normpath(
        abspath(join(dirname(__file__), "..", "data", "routemodel_gpx.csv"))
    )

    print(route_model_json_filepath, route_model_csv_filepath)

    if not os.path.exists(route_model_csv_filepath):
        df = gpx_json_to_df(route_model_json_filepath)
        df.to_csv(route_model_csv_filepath)
    seed_from_csv(route_model_csv_filepath)
    print("Success!")
