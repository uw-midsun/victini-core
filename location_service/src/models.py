import os
from geoalchemy2 import Geography

from . import db  # from __init__.py

tablename = f"location_service_{os.getenv('CONFIG_MODE')}"


class Location(db.Model):
    # Custom table name in database
    __tablename__ = tablename

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)

    coordinate = db.Column(
        Geography(geometry_type="POINT", srid=4326), nullable=False, unique=True
    )
    latitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    longitude = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
