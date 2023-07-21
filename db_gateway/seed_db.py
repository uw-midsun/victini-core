import csv
from app import create_app, db
from app.models.route import RoutePoints

def seed_database(csv_file):
    app = create_app()
    with app.app_context():
        db.create_all()

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
        
        db.session.commit()

if __name__ == '__main__':
    csv_file_path = r'./seed_data.csv'
    seed_database(csv_file_path)