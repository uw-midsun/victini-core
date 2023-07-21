from sqlalchemy import  Column, Integer, Float
from geoalchemy2 import Geometry

from app import db

class RoutePoints(db.Model):
  __tablename__ = "route"
  id = Column(Integer, primary_key=True)
  lat = Column(Float)
  lon = Column(Float)
  wkb_geometry = Column(Geometry("POINT", srid=4326, spatial_index=True))
  temperature = Column(Float)
  speed = Column(Float)

  def __init__(self, lat, lon, temperature, speed):
    self.lat = lat
    self.lon = lon
    self.temperature = temperature
    self.speed = speed
    self.wkb_geometry = f"POINT({lon} {lat})"

  # def __repr__(self):
  #   return f"Route(({self.lat}, {self.lon}), Temp: {self.temperature}, Ideal Speed: {self.speed})"
