from database import Base
from sqlalchemy import Column, Float, Integer, String


class RouteModel(Base):
    __tablename__ = "routemodel"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
    dir = Column(String, default=None)
    geopy_elapsed_dist_m = Column(Float)
    geopy_dist_from_last_m = Column(Float)
