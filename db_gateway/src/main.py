from database import db_session, reset_tables
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "--reset-tables",
    type=bool,
    help="If you want to reset all the tables managed by this service",
    required=False,
)
args = parser.parse_args()
args = vars(args)

app = Flask(__name__)
app.debug = True


app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    if args["reset_tables"]:
        reset_tables()
    app.run(debug=False, host="0.0.0.0", port=5001)
