import os

from . import create_app  # from __init__ file
from . import models

# App Initialization
app = create_app(os.getenv("CONFIG_MODE"))


# Routes/logics here
@app.route("/")
def hello():
    return "Hello World!"


# Start server
if __name__ == "__main__":
    # To Run the Server in Terminal => flask run -h localhost -p 5000
    # To Run the Server with Automatic Restart When Changes Occurred => FLASK_DEBUG=1 flask run -h localhost -p 5000
    app.run()
