import pandas as pd
import numpy as np
import json
from pathlib import Path
from sqlalchemy import create_engine, inspect, String
import geopandas as gpd
from geoalchemy2 import Geometry

def import_track_segments(track_data_filepath):
    file = Path(track_data_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")
    
    segments = {}
    dtypes = {'WKT': str, 'name': str, 'description': str}
    df = pd.read_csv(file, dtype=dtypes)
    df.dropna(subset=['WKT'], inplace=True)
    for _, row in df.iterrows():
        linestring, name = row['WKT'], row['name']
        linestring = linestring[12:-1]
        points = []
        for p in linestring.split(','):
            p = p.strip().split(' ')
            lng, lat = p[0], p[1]
            points.append(
                {
                    'lng': float(lng),
                    'lat': float(lat)
                }
            )
        segments[name] = points

    file_path = file.parent / f'{file.stem}_segments.json'
    with open(file_path, 'w') as f:
        json.dump(segments, f)
    return file_path


def construct_route(segments_data_filepath, segment_order, num_loops, route_name):
    file = Path(segments_data_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")

    segments = {}
    with open(file, 'r') as f:
        segments = json.load(f)

    segment_order = segment_order.split(' ')
    route_points = [segments[o] for o in segment_order]
    route = [point for rps in route_points * num_loops for point in rps]

    file_path = file.parent / f"{route_name}.json"
    with open(file_path, 'w') as f:
        json.dump(route, f)
    return file_path


# *In progress*
# def track_json_to_csv(route_file_path):
#     pass                                            


# *In progress*, copied from etl routemodel
# def seed_from_csv(track_csv_filepath, db_user, db_password, db_host, db_name):
#     file = Path(track_csv_filepath)
#     if not file.is_file():
#         raise FileNotFoundError("No file exists at the location specified")
#     gdf = gpd.GeoDataFrame(pd.read_csv(file))
#     gdf.fillna(np.nan).replace([np.nan], [None])
#     gdf.index.name = "id"
    
#     engine = create_engine(
#         f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
#     )

#     gdf.index += 1  # Making table 1-indexed
#     if inspect(engine).has_table("routemodel"):
#         row_len = pd.read_sql_query(sql="SELECT COUNT(*) FROM routemodel", con=engine)
#         gdf.index += row_len.iloc[0, 0]

#     response = gdf.to_sql(
#         name="routemodel",
#         con=engine,
#         schema="public",
#         if_exists="append",
#         index=True,
#         method="multi",
#         dtype={"geo": Geometry("POINT", srid=4326), "street_name": String},
#     )

#     if gdf.shape[0] != response:
#         raise SystemError("dataframe insertion failed")
#     else:
#         print("routemodel dataframe insertion success")
