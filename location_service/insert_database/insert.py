from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

df = pd.read_csv("location_service/insert_database/sample_coordinates.csv")

# INSERT_MODE can be 'fail', 'replace', or 'append'
INSERT_MODE = "replace"

with engine.connect() as connection:
    try:
        if INSERT_MODE == "fail":
            result = connection.execute(
                text("SELECT COUNT(*) FROM location_service.coordinates")
            )
            if result.scalar() > 0:
                raise Exception("Data already exists in the table")
        elif INSERT_MODE == "replace":
            print("Replacing the data in the database")
            connection.execute(text("DELETE FROM location_service.coordinates"))
        print("Inserting new data into location_service.coordinates")
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
        print("Success")
    except Exception as e:
        print(f"An error occurred: {e}")
