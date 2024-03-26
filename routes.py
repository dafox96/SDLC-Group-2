from flask import Flask, render_template, redirect, flash, url_for, session, request

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import User
from forms import login_form, register_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app: Flask = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for("library"))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template(
        "login.html",
        form=form,
        text="Login",
        title="Game Progress | Login",
        btn_action="Login",
    )


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                pwd=generate_password_hash(pwd).decode("utf8"),
            )

            db.session.add(newuser)
            db.session.commit()
            flash("Account successfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash("Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash("Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash("Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash("An error occurred", "danger")
    return render_template(
        "auth.html",
        form=form,
        text="Create account",
        title="Game Progress | Register",
        btn_action="Register account",
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/add-game")
def add_games():
    return render_template("add-game.html", title="Game Progress | Add Game")


@app.route("/library/")
def library():
    return render_template(
        "library.html",
        title="Game Progress | My Library",
        username=session.get("id", None),
    )


if __name__ == "__main__":
    app.run(debug=True)
