from database import Base
from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import backref, relationship


class RouteModel(Base):
    __tablename__ = "routemodel"
    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)
