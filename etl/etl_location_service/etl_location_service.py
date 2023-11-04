from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from geoalchemy2 import Geometry
from sqlalchemy import create_engine


def seed_from_csv(csv_filepath, db_user, db_password, db_host, db_name):
    file = Path(csv_filepath)
    if not file.is_file():
        raise FileNotFoundError("No file exists at the location specified")
    gdf = gpd.GeoDataFrame(pd.read_csv(file))
    gdf.fillna(np.nan).replace([np.nan], [None])
    gdf = gdf[["lat", "lon", "geo"]]
    gdf.index.name = "id"
    gdf.index += 1
    # gdf = gdf.head(10) # For testing purposes

    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    response = gdf.to_sql(
        name="location_service",
        con=engine,
        schema="public",
        if_exists="replace",
        index=True,
        method="multi",
        dtype={"geo": Geometry("POINT", srid=4326)},
    )
    if gdf.shape[0] != response:
        raise SystemError("dataframe insertion failed")
    else:
        print("location_service dataframe insertion success")


def main(csv_filepath, db_user, db_password, db_host, db_name):
    print("1) Parsing and seeding routemodel into location_service...")
    seed_from_csv(csv_filepath, db_user, db_password, db_host, db_name)


if __name__ == "__main__":
    csv_filepath = ""
    db_user = ""
    db_password = ""
    db_host = ""
    db_name = ""
    main(csv_filepath, db_user, db_password, db_host, db_name)
