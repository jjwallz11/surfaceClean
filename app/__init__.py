from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Settings

db = SQLAlchemy()
settings = Settings()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_ECHO'] = settings.SQLALCHEMY_ECHO

    db.init_app(app)

    # Import and register blueprints here later
    return app