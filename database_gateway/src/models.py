from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy.orm import validates

from . import db  # from __init__.py


class RouteModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)

    polyline_point_index = db.Column(db.Integer(), nullable=True)
    latitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    longitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    elevation_meters = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    elevation_gains_to_next_meters = db.Column(
        db.Numeric(precision=9, scale=6), nullable=False
    )
    elapsed_dist_meters = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    dist_to_next_coordinate_meters = db.Column(
        db.Numeric(precision=9, scale=6), nullable=True
    )
    true_bearing_to_next_coordinate = db.Column(
        db.Numeric(precision=9, scale=6), nullable=True
    )
    travel_direction = db.Column(db.String(), nullable=True)
    # add elevation grade, relative turning angles
