from flask import Flask
from os import getenv
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


# Flask constructor
def create_app():
    app = Flask(__name__)

    app.secret_key = getenv("LOGIN_SECRET")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///site.db"  # Using SQLite as the database
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    login_manager.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
