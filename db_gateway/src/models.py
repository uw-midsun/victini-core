from database import Base
from geoalchemy2 import Geometry
from geoalchemy2.comparator import Comparator
from sqlalchemy import Column, Float, ForeignKey, Integer, String


class RouteModel(Base):
    __tablename__ = "routemodel"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    geo = Column(Geometry(geometry_type="POINT", srid=4326))
    type = Column(String, default=None)
    street_name = Column(String, default=None)
    step = Column(String, default=None)
    next_turn = Column(String, default=None)
    dir = Column(String, default=None)
    speed_limit_km_per_h = Column(Float, default=None)
    gpx_dist_to_next_waypoint_m = Column(Float)
    gpx_elapsed_dist_m = Column(Float)
    geopy_elapsed_dist_m = Column(Float)
    geopy_dist_from_last_m = Column(Float)
    weather_id = Column(Integer)


class LocationService(Base):
    __tablename__ = "location_service"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    geo = Column(Geometry(geometry_type="POINT", srid=4326))


class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    cloud_cover = Column(Float)
