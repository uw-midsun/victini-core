import sys
from pathlib import Path

import psycopg2
import questionary
from etl_drop_tables.etl_drop_tables import main as run_drop_tables_etl
from etl_routemodel.etl_routemodel import main as run_routemodel_etl
from etl_weather.etl_weather import main as run_weather_etl
from etl_speed_limit.etl_speed_limit import main as run_speed_limit_etl
from etl_location_service.etl_location_service import main as run_location_service_etl
from termcolor import colored


def validate_db_creds():
    answers = questionary.form(
        db_host=questionary.text("Database host:port", default=""),
        db_name=questionary.text("Database name", default=""),
        db_user=questionary.text("Database user", default=""),
        db_password=questionary.password("Database user password", default=""),
    ).ask()
    db_user = answers["db_user"]
    db_password = answers["db_password"]
    db_host = answers["db_host"]
    db_name = answers["db_name"]
    host, port = db_host.split(":")
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=db_user, password=db_password, dbname=db_name
        )
        conn.close()
        return True, db_user, db_password, db_host, db_name
    except:
        return False, None, None, None, None


def validate_path(path, extension):
    path = Path(path).absolute()
    return path.is_file() and path.suffix == extension


def cmd_routemodel(db_user, db_password, db_host, db_name):
    answers = questionary.form(
        gpx_json_filepath=questionary.path(
            "Path to GPX data (JSON file)",
            default="",
            validate=lambda p: validate_path(p, ".json"),
        ),
        confirm=questionary.confirm(
            "Confirm routemodel ETL operation",
            default=False,
            auto_enter=False,
        ),
    ).ask()
    gpx_json_filepath = answers["gpx_json_filepath"]
    confirm = answers["confirm"]

    if not confirm:
        print(colored("routemodel ETL cancelled", "red"))
    else:
        run_routemodel_etl(gpx_json_filepath, db_user, db_password, db_host, db_name)
        print(colored("routemodel ETL success", "green"))


def cmd_location_service(db_user, db_password, db_host, db_name):
    answers = questionary.form(
        csv_filepath=questionary.path(
            "Path to data (CSV file)",
            default="",
            validate=lambda p: validate_path(p, ".csv"),
        ),
        confirm=questionary.confirm(
            "Confirm routemodel ETL operation",
            default=False,
            auto_enter=False,
        ),
    ).ask()
    csv_filepath = answers["csv_filepath"]
    confirm = answers["confirm"]

    if not confirm:
        print(colored("location_service ETL cancelled", "red"))
    else:
        run_location_service_etl(csv_filepath, db_user, db_password, db_host, db_name)
        print(colored("location_service ETL success", "green"))


def cmd_weather(db_user, db_password, db_host, db_name):
    answers = questionary.form(
        weather_range=questionary.text(
            "Weather range (number)", validate=lambda n: n.isnumeric()
        ),
        openweathermap_api_key=questionary.password(
            "Openweathermap API key", default=""
        ),
        confirm=questionary.confirm(
            "Confirm routemodel ETL operation",
            default=False,
            auto_enter=False,
        ),
    ).ask()
    weather_range = answers["weather_range"]
    openweathermap_api_key = answers["openweathermap_api_key"]
    confirm = answers["confirm"]

    if not confirm:
        print(colored("weather ETL cancelled", "red"))
    else:
        run_weather_etl(
            db_user,
            db_password,
            db_host,
            db_name,
            openweathermap_api_key,
            int(weather_range),
        )
        print(colored("weather ETL success", "green"))


def cmd_streetname_speedlimit(db_user, db_password, db_host, db_name):
    answers = questionary.form(
        bingmaps_api_key=questionary.password("Bing Maps API key", default=""),
        confirm=questionary.confirm(
            "Confirm street_name/speed_limit ETL operation",
            default=False,
            auto_enter=False,
        ),
    ).ask()
    bingmaps_api_key = answers["bingmaps_api_key"]
    confirm = answers["confirm"]

    if not confirm:
        print(colored("streetname/speedlimit ETL cancelled", "red"))
    else:
        run_speed_limit_etl(db_user, db_password, db_host, db_name, bingmaps_api_key)
        print(colored("streetname/speedlimit ETL success", "green"))


def cmd_drop_tables(db_user, db_password, db_host, db_name):
    answers = questionary.form(
        table_names=questionary.checkbox(
            "Select tables to drop",
            choices=[
                "routemodel",
                "weather",
            ],
            instruction="Use 'space' to select; 'enter' to continue",
        ),
        confirm=questionary.confirm(
            "Confirm routemodel ETL operation",
            default=False,
            auto_enter=False,
        ),
    ).ask()
    table_names = answers["table_names"]
    confirm = answers["confirm"]

    if not confirm:
        print(colored("drop tables ETL cancelled", "red"))
    else:
        run_drop_tables_etl(db_user, db_password, db_host, db_name, table_names)
        print(colored("drop tables ETL success", "green"))


if __name__ == "__main__":
    print(
        colored(
            "Using this ETL script requires your database to be updated and working with db_gateway",
            "yellow",
        )
    )
    etl_name = questionary.select(
        "Select ETL operation",
        choices=[
            "routemodel",
            "location_service",
            "weather",
            "speed_limit/street_names",
            "drop_tables",
        ],
    ).ask()

    auth, db_user, db_password, db_host, db_name = validate_db_creds()
    if auth is False:
        print(colored("Incorrect database credentials", "red"))
        sys.exit(1)

    if etl_name == "routemodel":
        cmd_routemodel(db_user, db_password, db_host, db_name)
    elif etl_name == "location_service":
        cmd_location_service(db_user, db_password, db_host, db_name)
    elif etl_name == "weather":
        cmd_weather(db_user, db_password, db_host, db_name)
    elif etl_name == "speed_limit/street_names":
        cmd_streetname_speedlimit(db_user, db_password, db_host, db_name)
    elif etl_name == "drop_tables":
        cmd_drop_tables(db_user, db_password, db_host, db_name)
