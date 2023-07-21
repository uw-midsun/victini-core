from flask import Blueprint, render_template
from sqlalchemy import text
from app import db

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    try:
        db.session.execute(text('SELECT 1'))  # Check if the connection to the database is successful
        message = "Connection to the database was successful!"
    except Exception as e:
        message = f"Failed to connect to the database: {e}"

    return render_template('index.html', message=message)