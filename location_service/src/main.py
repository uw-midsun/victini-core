import json
import os
from argparse import ArgumentParser

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.comparator import Comparator
from sqlalchemy import asc, func

load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")


parser = ArgumentParser()
parser.add_argument(
    "--create-table",
    type=bool,
    help="If you want a table to be created in the database",
    required=False,
)
parser.add_argument(
    "--seed-filename",
    type=str,
    help="String of the filepath of the csv file if you want to seed the database with the csv file contents",
    required=False,
)
args = parser.parse_args()
args = vars(args)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()


class Location(db.Model):
    __tablename__ = "location_test"  # Change table name

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    geo = db.Column(Geometry(geometry_type="POINT", srid=4326))

    def to_dict(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
        }

    @staticmethod
    def create(lat, lon):
        geo = "POINT({} {})".format(lon, lat)  # Note that postgis is (lon, lat)
        location = Location(lat=lat, lon=lon, geo=geo)
        db.session.add(location)
        db.session.commit()

    @staticmethod
    def seed_from_csv(filename):
        df = pd.read_csv(filename)
        db.session.query(Location).delete()
        for row in df.itertuples():
            geo = "POINT({} {})".format(
                row.longitude, row.latitude
            )  # Note that postgis is (lon, lat)
            location = Location(
                id=row.Index + 1, lat=row.latitude, lon=row.longitude, geo=geo
            )
            db.session.add(location)
        db.session.commit()


@app.route("/", methods=["GET"])
def index():
    return "location service"


@app.route("/all", methods=["GET"])
def all():
    locations = db.session.query(Location).order_by(asc(Location.id))
    return [l.to_dict() for l in locations]


@app.route("/location", methods=["POST"])
def closest_location():
    body = json.loads(request.data)
    lat = body.get("lat", None)
    lon = body.get("lon", None)
    if lat is None or lon is None:
        return "Invalid request body", 400
    location = (
        db.session.query(Location)
        .order_by(
            Comparator.distance_centroid(
                Location.geo,
                func.Geometry(
                    func.ST_GeographyFromText(
                        "POINT({} {})".format(lon, lat)
                    )  # Note that postgis is (lon, lat)
                ),
            )
        )
        .limit(1)
        .first()
    )
    return location.to_dict()


if __name__ == "__main__":
    if args["create_table"]:
        db.create_all()
    if args["seed_filename"]:
        Location.seed_from_csv(args["seed_filename"])
    app.run(debug=False, host="0.0.0.0", port=5000)
