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


# Moved the seed function to the etl folder

# def seed_from_csv(filename):
#     # import all modules here that might define models before calling init_db()
#     from models import RouteModel

#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     df = pd.read_csv(filename)
#     db_session.query(RouteModel).delete()
#     for row in df.itertuples():
#         location = RouteModel(
#             id=row.Index + 1,
#             lat=check_null(row.lat),
#             lon=check_null(row.lon),
#             type=check_null(row.type),
#             step=check_null(row.step),
#             next_turn=check_null(row.next_turn),
#             dir=check_null(row.dir),
#             gpx_dist_to_next_waypoint_m=check_null(row.gpx_dist_to_next_waypoint_m),
#             gpx_elapsed_dist_m=check_null(row.gpx_elapsed_dist_m),
#             geopy_elapsed_dist_m=check_null(row.geopy_elapsed_dist_m),
#             geopy_dist_from_last_m=check_null(row.geopy_dist_from_last_m),
#         )
#         db_session.add(location)
#     db_session.commit()
