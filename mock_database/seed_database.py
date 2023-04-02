#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine

# You will primarily work with the global variables here
MYSQL_HOST = "localhost"
MYSQL_DATABASE = "midsun_dev_db_mock"
MYSQL_USER = "user"
MYSQL_PASSWORD = "password"

CSV_FILE = "sample_data.csv"  # file path is relative to this file
DB_TABLE_NAME = "sample_data_table"


def to_dataframe(csv_file=CSV_FILE):
    """
    to_dataframe is a function to load a csv file as a pandas dataframe
    @param csv_file: the name of the csv file that is to be loaded to a dataframe
    @return: A pandas dataframe
    """
    df = pd.read_csv(CSV_FILE)
    return df


def to_database(
    dataframe,
    table_name=DB_TABLE_NAME,
    database_name=MYSQL_DATABASE,
    if_exists="replace",
    mysql_host=MYSQL_HOST,
    mysql_user=MYSQL_USER,
    mysql_password=MYSQL_PASSWORD,
):
    """
    to_database is a function to save a Pandas dataframe into a database
    @param dataframe: the dataframe that contains the data to be put into the database
    @param table_name: the name of the table that the data is to be saved into
    @param database_name: the name of the database
    @param if_exists: action to do if the table already exists in the database (options: 'fail', 'replace', 'append')
    @param mysql_host: where the mysql database is hosted
    @param mysql_user: mysql username
    @param mysql_password: mysql password
    @return: None
    """
    engine = create_engine(
        f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{database_name}"
    )
    data = dataframe.fillna("")

    if data is not None:
        response = data.to_sql(
            name=table_name, con=engine, if_exists=if_exists, method="multi"
        )

        rowcount = data.shape[0]
        if rowcount != response:
            raise Exception(
                f"dataframe was not successfully inserted into the '{table_name}' table in the {database_name} database"
            )
    else:
        Exception("csv file was empty")


if __name__ == "__main__":
    data = to_dataframe()
    to_database(data)
