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
Base = declarative_base()
Base.query = db_session.query_property()


def seed_from_csv(filename):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import RouteModel

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    df = pd.read_csv(filename)
    db_session.query(RouteModel).delete()
    for row in df.itertuples():
        location = RouteModel(id=row.Index + 1, lat=row.lat, lon=row.lon)
        db_session.add(location)
    db_session.commit()
