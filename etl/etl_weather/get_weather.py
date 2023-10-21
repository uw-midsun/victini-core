import requests
import sys

import os
from dotenv import load_dotenv

load_dotenv()


ONE_CALL_BASE = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")

print("API KEY", API_KEY)


def get_weather(lat, long):
    """
    Calls OpenWeather API to get wind data and returns data in a dict
    @param lat: string containing latitude value
    @param long: string containing longitude value
    @return: dict containing the weather data
    """
    units = "metric"
    exclude = "minutely,hourly,daily,alerts"  # To exclude certain weather reports, right now just using current
    url = ONE_CALL_BASE + "lat={}&lon={}&units={}&appid={}".format(
        lat, long, units, API_KEY
    )
    print("URL", url)
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        print(weather_data)

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

    print("An error occurred: ", response.json())
    sys.exit()
