import csv
from app import create_app, db
from app.models.route import RoutePoints
from sqlalchemy import select

from argparse import ArgumentParser

def seed_database(csv_file, drop_db=False):
    app = create_app()
    with app.app_context():

        if drop_db:
            db.drop_all()
            db.create_all()

        if db.session.query(RoutePoints).first() is not None:
            print("Database contains data. Use --drop to delete existing data.")
            return
        
        
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                route = RoutePoints(
                    float(row['latitude']), 
                    float(row['longitude']), 
                    float(row['temperature']), 
                    float(row['speed'])
                )
                db.session.add(route)
            print("Seeding database...")
        
        db.session.commit()
        print("Database seeded!")

if __name__ == '__main__':
    csv_file_path = r'./seed_data.csv'

    parser = ArgumentParser()
    parser.add_argument('--drop', action='store_true')
    args = parser.parse_args()

    seed_database(csv_file_path, args.drop)