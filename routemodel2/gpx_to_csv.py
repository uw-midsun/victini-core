import pandas as pd
import json
from bs4 import BeautifulSoup
from geopy import distance


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


if __name__ == "__main__":
    df = gpx_json_to_df("./uw_sample_gpx.json")
    print(df)
    df.to_csv("uw_sample_gpx.csv")
