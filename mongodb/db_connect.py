from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
from bson.json_util import dumps

load_dotenv()
mongo_url = os.getenv('MONGO_URL')

def connect():
    client = MongoClient(mongo_url)
    try:
        client.admin.command('ping')
        print('Connected to MongoDB')
    except Exception as e:
        print('Failed to connect to MongoDB', e, file=sys.stderr)
        
    return client

def check_change(client: MongoClient):
    change_stream = client['race-data']['car-location'].watch([{
        '$match': {
            'operationType': { '$in': ['insert'] }
        }
    }])
    for change in change_stream:
        print(dumps(change))
        print('') # for readability only

def main():
    client = connect()
    check_change(client)

if __name__ == "__main__":
    main()
