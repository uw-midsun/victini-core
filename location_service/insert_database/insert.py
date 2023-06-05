from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

# load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Put path to csv file here
df = pd.read_csv("./location_service/insert_database/sample_coordinates.csv")


if __name__ == "__main__":
    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    with engine.connect() as connection:
        try:
            for index, row in df.iterrows():
                stmt = text(
                    "INSERT INTO location_service.coordinates (coordinates, latitude, longitude) VALUES (ST_GeomFromText(:coordinates, 4326), :latitude, :longitude)"
                )
                params = {
                    "coordinates": f"POINT({row.latitude} {row.longitude})",
                    "latitude": row.latitude,
                    "longitude": row.longitude,
                }
                connection.execute(stmt, params)
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
