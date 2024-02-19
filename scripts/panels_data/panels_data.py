from sqlalchemy import create_engine, MetaData, Column, Integer, String, Float, Table
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


# creating Panel class to declare the structure of the database table and define what the entries look like
class Panel(Base):
    __tablename__ = "panels_data"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    stack = Column(Integer(), nullable=False)
    efficiency = Column(Float(), nullable=False)
    num_panels = Column(Integer(), nullable=False)
    tilt = Column(Float(), nullable=False)
    width = Column(Float(), nullable=False)
    height = Column(Float(), nullable=False)
    area = Column(Float(), nullable=False)


def create_panel_table(db_user, db_password, db_host, db_name):
    # connecting to database
    engine = create_engine(
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # used to check if table exists
    metadata = MetaData()
    panel_table = Table(
        "panels_data",
        metadata,
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("name", String(100), nullable=False, unique=True),
        Column("stack", Integer(), nullable=False),
        Column("efficiency", Float(), nullable=False),
        Column("num_panels", Integer(), nullable=False),
        Column("tilt", Float(), nullable=False),
        Column("width", Float(), nullable=False),
        Column("height", Float(), nullable=False),
        Column("area", Float(), nullable=False)
    )
    panel_area = 0.0153

    # drop if exists
    panel_table.drop(engine, checkfirst=True)

    # create table
    metadata.create_all(engine, checkfirst=True)

    # setting entry values
    panel_data = [
        {
            "name": "Back Left 1",
            "stack": 7,
            "efficiency": 0.25,
            "num_panels": 28,
            "tilt": -8.28,
            "width": 0.5,
            "height": 0.875,
            "area": 28*panel_area
        },
        {
            "name": "Back Right 1",
            "stack": 8,
            "efficiency": 0.25,
            "num_panels": 28,
            "tilt": -8.28,
            "width": 0.5,
            "height": 0.875,
            "area": 28*panel_area
        },
        {
            "name": "Back Middle 1",
            "stack": 3,
            "efficiency": 0.25,
            "num_panels": 12,
            "tilt": -8.06,
            "width": 0.25,
            "height": 0.75,
            "area": 12*panel_area
        },
        {
            "name": "Back Left 2",
            "stack": 9,
            "efficiency": 0.25,
            "num_panels": 28,
            "tilt": -5.21,
            "width": 0.5,
            "height": 0.875,
            "area": 28*panel_area
        },
        {
            "name": "Back Right 2",
            "stack": 10,
            "efficiency": 0.25,
            "num_panels": 28,
            "tilt": -5.21,
            "width": 0.5,
            "height": 0.875,
            "area": 28*panel_area
        },
        {
            "name": "Back Middle 2",
            "stack": 1,
            "efficiency": 0.25,
            "num_panels": 21,
            "tilt": -5.21,
            "width": 0.375,
            "height": 0.875,
            "area": 21*panel_area
        },
        {
            "name": "Middle Left 1",
            "stack": 15,
            "efficiency": 0.25,
            "num_panels": 18,
            "tilt": -2.14,
            "width": 0.375,
            "height": 0.75,
            "area": 18*panel_area
        },
        {
            "name": "Middle Right 1",
            "stack": 16,
            "efficiency": 0.25,
            "num_panels": 18,
            "tilt": -2.14,
            "width": 0.375,
            "height": 0.75,
            "area": 18*panel_area
        },
        {
            "name": "Middle Left 2",
            "stack": 4,
            "efficiency": 0.25,
            "num_panels": 10,
            "tilt": 0.77,
            "width": 0.25,
            "height": 0.625,
            "area": 10*panel_area
        },
        {
            "name": "Middle Right 2",
            "stack": 4,
            "efficiency": 0.25,
            "num_panels": 10,
            "tilt": 0.77,
            "width": 0.25,
            "height": 0.625,
            "area": 10*panel_area
        },
        {
            "name": "Front Left",
            "stack": 13,
            "efficiency": 0.25,
            "num_panels": 21,
            "tilt": 5.13,
            "width": 0.375,
            "height": 0.875,
            "area": 21*panel_area
        },
        {
            "name": "Front Right",
            "stack": 2,
            "efficiency": 0.25,
            "num_panels": 21,
            "tilt": 5.13,
            "width": 0.375,
            "height": 0.875,
            "area": 21*panel_area
        },
        {
            "name": "Front Middle",
            "stack": 11,
            "efficiency": 0.25,
            "num_panels": 16,
            "tilt": 8.75,
            "width": 0.5,
            "height": 0.5,
            "area": 16*panel_area
        },
    ]
    # unpacking each entry to create a Panel instance and adding to table
    for data in panel_data:
        panel = Panel(**data)
        session.add(panel)

    # upload to database
    session.commit()
    print("Table added successfully.")
    # disconnect
    engine.dispose()


def main(db_user, db_password, db_host, db_name):
    print("Uploading solar panel data into panel_data...")
    create_panel_table(db_user, db_password, db_host, db_name)


# allows it to be run as a script
if __name__ == "__main__":
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOSTNAME")
    db_name = os.getenv("DB_NAME")
    main(db_user, db_password, db_host, db_name)
