import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
DATABASE_URI = os.environ.get("DATABASE_URI")

engine = create_engine(
    DATABASE_URI,
    convert_unicode=True,
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base(bind=engine)
Base.query = db_session.query_property()


def check_null(value):
    return None if pd.isnull(value) else value


def reset_tables():
    from models import RouteModel, Weather, LocationService

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
