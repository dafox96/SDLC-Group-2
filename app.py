from flask import Flask, request, render_template, redirect, url_for
from os import getenv
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

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

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
