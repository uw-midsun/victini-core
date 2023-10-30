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

sys.path.append(normpath(abspath(join(dirname(__file__), "..", ".."))))

# Import database information from db_gateway
# Note, it's important to import the Base instead of redeclaring, otherwise create_all() will fail
from db_gateway.src.database import Base, engine, db_session

# How many meters between each weather API call
WEATHER_RANGE = 30000


# The logic for this function is WIP, currently it takes a 1 hour forecast for each point starting from the current time
# Comments with POI will point you towards where you should adjust parameters if you want the forecast to be offset from the current time
def weather_api_to_df():
    from get_weather import get_weather
    from db_gateway.src.models import RouteModel

    df_rows = []

    # Go through the RouteModel table and every 30 miles make a call to the weather API
    # Save the weather data to a dataframe
    routemodel = db_session.query(RouteModel)

    idx = 0
    for point in routemodel:
        if point.geopy_elapsed_dist_m >= WEATHER_RANGE * idx:
            idx += 1
            print(
                "Making {}th weather call at ".format(idx),
                point.lat,
                point.lon,
                "at distance",
                point.geopy_elapsed_dist_m,
            )

            # POI: Make the API call
            weather_data = get_weather(point.lat, point.lon)

            print(weather_data)

            if not weather_data:
                print("No response from API")
                continue

            # Add the weather data to a dataframe
            data = {
                "id": idx,
                "lat": point.lat,
                "lon": point.lon,
                "temperature": weather_data["Temperature (C)"],
                "humidity": weather_data["Humidity"],
                "wind_speed": weather_data["Wind Speed (m/s)"],
                "wind_direction": weather_data["Wind Direction"],
                "cloud_cover": weather_data["Cloud Cover"],
            }

            df_rows.append(data)

    return pd.DataFrame(df_rows)


# Step 2


def check_null(value):
    return None if pd.isnull(value) else value


def seed_from_csv(filename):
    # import all modules here that might define models before calling init_db()
    from db_gateway.src.models import RouteModel, Weather

    if (
        engine.has_table(engine, Weather.__tablename__)
        and not db_session.query(Weather).count() == 0
    ):
        print("Table exists and contains values, skipping seed")
        return

    Base.metadata.create_all(bind=engine, tables=[Weather.__table__])

    # Add Weather Table
    df = pd.read_csv(filename)
    for row in df.itertuples():
        location = Weather(
            id=row.Index + 1,
            lat=check_null(row.lat),
            lon=check_null(row.lon),
            temperature=check_null(row.temperature),
            humidity=check_null(row.humidity),
            wind_speed=check_null(row.wind_speed),
            wind_direction=check_null(row.wind_direction),
            cloud_cover=check_null(row.cloud_cover),
        )
        db_session.add(location)
    db_session.commit()

    routemodel = db_session.query(RouteModel).order_by(RouteModel.id)
    # Get the geopy_dist for the last point in route model
    last_point = routemodel[-1]
    last_point_dist = last_point.geopy_elapsed_dist_m

    print("Furthest race point is {} meters away".format(last_point_dist))
    for i in range(int(last_point_dist // WEATHER_RANGE) + 1):
        start = i * WEATHER_RANGE
        end = (i + 1) * WEATHER_RANGE

        print("Updated ranges", start, end, "with weather id", i + 1)

        db_session.query(RouteModel).filter(
            RouteModel.geopy_elapsed_dist_m >= start,
            RouteModel.geopy_elapsed_dist_m < end,
        ).update({"weather_id": i + 1}, synchronize_session=False)

    db_session.commit()


if __name__ == "__main__":
    weather_csv_filepath = normpath(
        abspath(join(dirname(__file__), "..", "data", "weather.csv"))
    )

    if not os.path.exists(weather_csv_filepath):
        # We'll read from the database to get the lat/lon values
        df = weather_api_to_df()
        df.to_csv(weather_csv_filepath)
    # After generating a csv of the weather data, we'll read from it to generate the Weather table, this allows us to reseed the Weather data without repeatedly using API calls
    seed_from_csv(weather_csv_filepath)
    print("Success!")
