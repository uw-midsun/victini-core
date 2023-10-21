from database import Base
from sqlalchemy import Column, Float, Integer, String, ForeignKey

class RouteModel(Base):
    __tablename__ = "routemodel"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    type = Column(String, default=None)
    step = Column(String, default=None)
    next_turn = Column(String, default=None)
    dir = Column(String, default=None)
    gpx_dist_to_next_waypoint_m = Column(Float)
    gpx_elapsed_dist_m = Column(Float)
    geopy_elapsed_dist_m = Column(Float)
    geopy_dist_from_last_m = Column(Float)
    weather_id = Column(Integer, ForeignKey('weather.id'))

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