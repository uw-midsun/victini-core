from flask import Blueprint, render_template, jsonify
from app.models.route import RoutePoints
from sqlalchemy.exc import SQLAlchemyError
from app import db

route_bp = Blueprint('route_bp', __name__, url_prefix='/routes')

@route_bp.route('/')
def index():
    route = RoutePoints.query.all()
    return render_template('routes.html', route=route)
