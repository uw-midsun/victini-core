import json
import os

from dotenv import load_dotenv
from flask import Flask, request
from update_weather import update_weather

load_dotenv()
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

AUTH_KEY = os.environ.get("AUTH_KEY")
FLASK_APP_PORT = os.environ.get("FLASK_APP_PORT")
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")


app = Flask(__name__)


def authorized(auth_key):
    return auth_key == AUTH_KEY


@app.route("/", methods=["GET"])
def index():
    return "update weather service"


@app.route("/update-weather", methods=["POST"])
def update_weather():
    body = json.loads(request.data)
    auth_key = body.get("auth_key", None)
    id = body.get("id", None)
    if not authorized(auth_key):
        return "Not authorized", 401
    if id is None or int(id) < 1:
        return "Invalid request body", 400

    res, status = update_weather(
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_HOST,
        DATABASE_NAME,
        OPENWEATHERMAP_API_KEY,
        weather_row_id=int(id),
    )
    return res, status


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=FLASK_APP_PORT)
