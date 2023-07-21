from argparse import ArgumentParser
from app import create_app, db
from app.models.route import RoutePoints

def create_tables(app):
	with app.app_context():
		db.create_all()

def main():
	parser = ArgumentParser()
	parser.add_argument("--create-tables", action="store_true", help="If you want a table to be created in the database")
	args = parser.parse_args()

	app = create_app()

	if args.create_tables:
		create_tables(app)
	
	app.run(debug=True)

if __name__ == '__main__':
		main()