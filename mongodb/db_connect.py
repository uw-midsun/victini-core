from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
from bson.json_util import dumps
from docker_commands import on_insert

load_dotenv()
mongo_url = os.getenv('MONGO_URL')


def connect():
    '''
    Connect to MongoDB and return the client.
    Pings the database to check if the connection is successful.
    Throws an error and exits if the connection fails.
    '''
    client = MongoClient(mongo_url)
    try:
        client.admin.command('ping')
        print('Connected to MongoDB')
    except Exception as e:
        print('Failed to connect to MongoDB', e, file=sys.stderr)
        
    return client


def check_change(client: MongoClient):
    '''
    Tracks changes in the database and calls the on_insert function when a new document is inserted.
    Parameters:
        client: The MongoDB client.
    Runs indefinitely until the program is stopped.
    '''
    change_stream = client['race-data']['car-location'].watch([{
        '$match': {'operationType': { '$in': ['insert'] }}
    }])
    for change in change_stream:
        print(dumps(change))
        print('')  # for readability only
        on_insert(change['fullDocument'])


def main():
    client = connect()  # Connect to MongoDB
    check_change(client)  # Track changes in the database


if __name__ == "__main__":
    main()
