from pathlib import Path

import psycopg2
import questionary
from termcolor import colored
from etl_routemodel.etl_routemodel import main as run_routemodel_etl
from etl_weather.etl_weather import main as run_weather_etl


def validate_db_creds(db_user, db_password, db_host, db_name):
    host, port = db_host.split(":")
    try:
        conn = psycopg2.connect(
            host=host, port=port, user=db_user, password=db_password, dbname=db_name
        )
        conn.close()
        return True
    except:
        return False


def validate_path(path, extension):
    path = Path(path).absolute()
    return path.is_file() and path.suffix == extension


def cmd_routemodel():
    answers = questionary.form(
        gpx_json_filepath=questionary.path(
            "Path to GPX data (JSON file)",
            default="",
            validate=lambda p: validate_path(p, ".json"),
        ),
        db_host=questionary.text("Database host:port", default=""),
        db_name=questionary.text("Database name", default=""),
        db_user=questionary.text("Database user", default=""),
        db_password=questionary.password("Database user password", default=""),
        confirm=questionary.confirm(
            "Confirm routemodel ETL operation",
            default=False,
            auto_enter=False,
        ),
    ).ask()

    gpx_json_filepath, db_user, db_password, db_host, db_name, confirm = map(
        answers.get,
        (
            "gpx_json_filepath",
            "db_user",
            "db_password",
            "db_host",
            "db_name",
            "confirm",
        ),
    )
    if not confirm:
        print(colored("routemodel ETL cancelled", "red"))
    elif confirm and validate_db_creds(db_user, db_password, db_host, db_name):
        run_routemodel_etl(gpx_json_filepath, db_user, db_password, db_host, db_name)
        print(colored("routemodel ETL success", "green"))
    else:
        print(colored("Incorrect database credentials", "red"))


def cmd_weather():
    answers = questionary.form(
        db_host=questionary.text("Database host:port", default=""),
        db_name=questionary.text("Database name", default=""),
        db_user=questionary.text("Database user", default=""),
        db_password=questionary.password("Database user password", default=""),
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

    (
        db_host,
        db_name,
        db_user,
        db_password,
        weather_range,
        openweathermap_api_key,
        confirm,
    ) = map(
        answers.get,
        (
            "db_host",
            "db_name",
            "db_user",
            "db_password",
            "weather_range",
            "openweathermap_api_key",
            "confirm",
        ),
    )
    if not confirm:
        print(colored("weather ETL cancelled", "red"))
    elif confirm and validate_db_creds(db_user, db_password, db_host, db_name):
        run_weather_etl(
            db_user,
            db_password,
            db_host,
            db_name,
            openweathermap_api_key,
            int(weather_range),
        )
        print(colored("weather ETL success", "green"))
    else:
        print(colored("Incorrect database credentials", "red"))


if __name__ == "__main__":
    print(
        colored(
            "Using this ETL script requires your database to be updated and working with db_gateway",
            "yellow",
        )
    )
    etl_name = questionary.select(
        "Select ETL operation", choices=["routemodel", "weather"]
    ).ask()

    if etl_name == "routemodel":
        cmd_routemodel()
    elif etl_name == "weather":
        cmd_weather()
