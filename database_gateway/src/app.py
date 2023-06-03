import json
import os

from flask import request

from . import create_app  # from __init__ file
from . import models, utils


# App Initialization
app = create_app(os.getenv("CONFIG_MODE"))


# Routes
@app.route("/")
def index():
    return "Victini Database Gateway Running!"


@app.route("/routemodel", methods=["GET"])
def get_by_id():
    data = json.loads(request.data)
    table_name = data.get("table_name")
    table_index = data.get("table_index")
    api_key = data.get("api_key")

    if None in [table_name, table_index, api_key]:
        return {"info": "Incorrect or missing data in request body"}, 400
    if not utils.verify_api_key(api_key):
        return {"info": "Unathorized"}, 401


# Start server
# To Run the Server in Terminal => flask run -h localhost -p 5000
# To Run the Server with Automatic Restart When Changes Occurred => FLASK_DEBUG=1 flask run -h localhost -p 5000
if __name__ == "__main__":
    app.run()
