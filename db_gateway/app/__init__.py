from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.views.route_view import route_bp
    from app.views.index_view import index_bp

    app.register_blueprint(route_bp, url_prefix='/routes')
    app.register_blueprint(index_bp)

    return app