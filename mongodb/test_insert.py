from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv

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

def main():
    client = connect()
    print(client['race-data']['car-location'].insert_one({"location":{"Lattitude":{"N":"60.15334714532838"},"Longitude":{"N":"4.407109787976424"}},"Speed":{"$numberInt":"40"}}).inserted_id)
    
if __name__ == '__main__':
    main()
