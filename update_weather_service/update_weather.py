import pandas as pd
from sqlalchemy import create_engine, inspect
from datetime import datetime
import requests

API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(lat, long, API_KEY):  # Copied from etl_weather
    units = "metric"
    exclude = "minutely,hourly,daily,alerts"  # To exclude certain weather reports, right now just using current
    url = f"{API_BASE_URL}?lat={lat}&lon={long}&units={units}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(response.json())
        raise response.raise_for_status()

    weather_data = response.json()
    precipitation = (
        0
        if "rain" not in weather_data
        else weather_data["rain"]["1h"] or weather_data["rain"]["3h"]
    )
    weather_dict = {
        "Latitude": lat,
        "Longitude": long,
        "Temperature (C)": weather_data["main"]["temp"],
        "Wind Speed (m/s)": weather_data["wind"]["speed"],
        "Wind Direction": weather_data["wind"]["deg"],
        "Weather": weather_data["weather"][0]["main"],
        "Weather Description": weather_data["weather"][0]["description"],
        "Pressure (hPa)": weather_data["main"]["pressure"],
        "Precipitation (mm)": precipitation,
        "Cloud Cover": weather_data["clouds"]["all"],
        "Humidity": weather_data["main"]["humidity"],
    }
    return weather_dict


def update_weather(db_user, db_password, db_host, db_name, API_KEY, weather_row_id=1):
    assert weather_row_id >= 1
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    if not inspect(engine).has_table("weather"):
        raise SystemError("weather table does not exist in database")
    weather_df = pd.read_sql_query(sql="SELECT * FROM weather", con=engine)
    weather_df.index += 1  # Make it 1-indexed
    weather_df_len = len(weather_df) + 1

    if weather_row_id >= weather_df_len:
        return (
            f"weather_row_id {weather_row_id} exceeds number of weather rows ({len(weather_df)})",
            404,
        )

    print(f"Updating weather data from id {weather_row_id}...")
    for i in range(weather_row_id, weather_df_len):
        lat = weather_df.loc[i, "lat"]
        lon = weather_df.loc[i, "lon"]
        weather_data = get_weather(lat, lon, API_KEY)
        weather_df.loc[i, "temperature"] = weather_data["Temperature (C)"]
        weather_df.loc[i, "humidity"] = weather_data["Humidity"]
        weather_df.loc[i, "wind_speed"] = weather_data["Wind Speed (m/s)"]
        weather_df.loc[i, "wind_direction"] = weather_data["Wind Direction"]
        weather_df.loc[i, "cloud_cover"] = weather_data["Cloud Cover"]

    weather_response = weather_df.to_sql(
        name="weather",
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        method="multi",
    )
    if weather_df.shape[0] != weather_response:
        raise SystemError("weather table update failed")
    res = f"weather table starting at id={weather_row_id} updated at {datetime.now().strftime('%m/%d/%Y %H:%M:%S')}"
    print(res)
    return res, 200


if __name__ == "__main__":
    db_user = ""
    db_password = ""
    db_host = ""
    db_name = ""
    API_KEY = ""
    weather_row_id = 1
    update_weather(
        db_user,
        db_password,
        db_host,
        db_name,
        API_KEY,
        weather_row_id,
    )
