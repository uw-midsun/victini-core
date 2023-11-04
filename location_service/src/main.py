import json
import os

from dotenv import load_dotenv
from flask import Flask, request
from psycopg2 import pool as psycopg2_pool

load_dotenv()
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "False").lower() in ("true", "1", "t")
AUTH_KEY = os.environ.get("AUTH_KEY")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


app = Flask(__name__)
postgres_pool = psycopg2_pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)


def authorized(auth_key):
    if not REQUIRE_AUTH:
        return True
    return auth_key == AUTH_KEY


@app.route("/", methods=["GET"])
def index():
    return "location service"


@app.route("/all", methods=["GET", "POST"])
def all():
    body = json.loads(request.data)
    auth_key = body.get("auth_key", None)
    if not authorized(auth_key):
        return "Not authorized", 401

    query = "SELECT id, lat, lon FROM location_service;"
    conn = postgres_pool.getconn()
    cur = conn.cursor()
    cur.execute(query)
    locations = [dict(zip(("id", "lat", "lon"), values)) for values in cur.fetchall()]
    cur.close()
    postgres_pool.putconn(conn)
    return locations


@app.route("/location", methods=["POST"])
def closest_location():
    body = json.loads(request.data)
    lat = body.get("lat", None)
    lon = body.get("lon", None)
    auth_key = body.get("auth_key", None)
    if not authorized(auth_key):
        return "Not authorized", 401
    if lat is None or lon is None:
        return "Invalid request body", 400

    query = f"""
    SELECT *
    FROM location_service 
    ORDER BY location_service.geo <-> ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326)
    LIMIT 1;
    """
    conn = postgres_pool.getconn()
    cur = conn.cursor()
    cur.execute(query)
    location = dict(zip(("id", "lat", "lon"), cur.fetchone()))
    cur.close()
    postgres_pool.putconn(conn)
    return location


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
