import json
from pathlib import Path

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from geopy import distance
from sqlalchemy import create_engine, inspect


def gpx_json_to_df(json_filepath):
    file = Path(json_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")

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

    df = pd.DataFrame(df_rows)
    csv_filepath = file.with_suffix(".csv")
    if not csv_filepath.is_file():
        df.to_csv(csv_filepath)
    return csv_filepath


def seed_from_csv(csv_filepath, db_user, db_password, db_host, db_name):
    file = Path(csv_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")
    df = pd.read_csv(file)
    df.fillna(np.nan).replace([np.nan], [None])
    df = df.drop(columns=["Unnamed: 0"])
    # df = df.head(10) # For testing purposes

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    df.index += 1  # Making table 1-indexed
    if inspect(engine).has_table("routemodel"):
        row_len = pd.read_sql_query(sql="SELECT COUNT(*) FROM routemodel", con=engine)
        df.index += row_len.iloc[0, 0]

    response = df.to_sql(
        name="routemodel",
        con=engine,
        schema="public",
        if_exists="append",
        index=True,
        method="multi",
    )
    if df.shape[0] != response:
        raise SystemError("dataframe insertion failed")
    else:
        print("dataframe insertion success")


def main(gpx_json_filepath, db_user, db_password, db_host, db_name):
    csv_filepath = gpx_json_to_df(gpx_json_filepath)
    seed_from_csv(csv_filepath, db_user, db_password, db_host, db_name)


if __name__ == "__main__":
    gpx_json_filepath = ""
    db_user = ""
    db_password = ""
    db_host = ""
    db_name = ""
    main(gpx_json_filepath, db_user, db_password, db_host, db_name)
