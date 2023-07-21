from flask import Blueprint, render_template
from app.models.route import RoutePoints

route_bp = Blueprint('route_bp', __name__, url_prefix='/routes')

@route_bp.route('/')
def index():
    route = RoutePoints.query.all()
    return render_template('routes.html', route=route)