from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
from car_data import CarData, Location

load_dotenv()
# The MONGO_URL environment variable is set in the .env file
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
        exit (1)
        
    return client

def main():
    client = connect()
    # Creating a new record for testing purposes
    insert_record: CarData = CarData(location=Location(Lattitude={'N': '60.15334714532838'}, Longitude={'N': '4.407109787976424'}), speed=40)
    # Printing the record's inserted_id to the console
    print(client['race-data']['car-location'].insert_one(insert_record.model_dump()).inserted_id)
    
if __name__ == '__main__':
    main()
