import os
import threading
import time
import logging

import schedule
from dotenv import load_dotenv
from utils import connected_to_internet
from update_weather.update_weather import update_weather

# Env vars
load_dotenv()
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
AUTH_KEY = os.environ.get("AUTH_KEY")
FLASK_APP_PORT = os.environ.get("FLASK_APP_PORT")
OPENWEATHERMAP_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")


def threaded_update_weather(weather_row_id=1):
    if connected_to_internet():
        thread = threading.Thread(
            target=update_weather,
            name="update_weather_thread",
            daemon=True,
            args=(
                DATABASE_USER,
                DATABASE_PASSWORD,
                DATABASE_HOST,
                DATABASE_NAME,
                OPENWEATHERMAP_API_KEY,
                weather_row_id,
            ),
        )
        thread.start()


# def print_hi():
#     time.sleep(10)
#     logging.info("Hi")


# def thread_test():
#     thread = threading.Thread(
#         target=print_hi,
#         name="print_hi_thread",
#     )
#     thread.start()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="TID-%(thread)d | %(threadName)s: %(message)s"
    )
    schedule.every(30).seconds.do(threaded_update_weather, 15)
    schedule.every(30).seconds.do(threaded_update_weather, 1)

    while True:
        thread_names = ", ".join(thread.name for thread in threading.enumerate())
        logging.info(f"{threading.active_count()} active threads: {thread_names}")
        schedule.run_pending()
        time.sleep(5)
