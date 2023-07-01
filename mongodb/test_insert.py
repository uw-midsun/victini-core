from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
from car_data import CarData, Location

load_dotenv()
mongo_url = os.getenv('MONGO_URL')

def connect():
    client = MongoClient(mongo_url)
    try:
        client.admin.command('ping')
        print('Connected to MongoDB')
    except Exception as e:
        print('Failed to connect to MongoDB', e, file=sys.stderr)
        exit (1)
        
    return client

def main():
    client = connect()
    insert_record: CarData = CarData(location=Location(Lattitude={'N': '60.15334714532838'}, Longitude={'N': '4.407109787976424'}), speed=40)
    print(client['race-data']['car-location'].insert_one(insert_record.model_dump()).inserted_id)
    
if __name__ == '__main__':
    main()
