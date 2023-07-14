import pandas as pd
import json
from bs4 import BeautifulSoup


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
            "dist_to_next_m": None,
            "elapsed_dist_m": None,
            "time_to_next_s": None,
        }
        if dir := point.get("dir", None):
            soup = BeautifulSoup(dir, "html.parser")
            data["dir"] = soup.get_text()
        if dist := point.get("dist", None):
            data["elapsed_dist_m"] = dist["total"] - dist["val"]
            data["dist_to_next_m"] = dist["val"]
        if time := point.get("timeto", None):
            data["time_to_next_s"] = time["val"]
        df_rows.append(data)
    return pd.DataFrame(df_rows)


if __name__ == "__main__":
    df = gpx_json_to_df("./uw_sample_gpx.json")
    print(df)
    df.to_csv("uw_sample_gpx.csv")
