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
from models import User, Game
from forms import login_form, register_form, add_game_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app: Flask = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Game Progress App | Home")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.pwd, form.pwd.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for("library"))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")

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
            pwd: str | None = form.pwd.data
            username: str | None = form.username.data

            new_user = User(
                username=username,
                pwd=generate_password_hash(pwd).decode(
                    "utf8"
                ),  # Hash password before storing
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully created", "success")
            return redirect(url_for("library"))

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
        btn_action="Register Account",
    )


@app.route("/logout")
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for("login"))


@app.route("/library/add-game/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def add_games():
    form = add_game_form()
    if form.validate_on_submit():
        try:
            game_title: str | None = form.game_title.data
            game_progress: int | None = form.game_progress.data

            new_game = Game(game_title=game_title, game_progress=game_progress)

            user = User.query.filter_by(id=current_user.id).first()
            user.games.append(new_game)

            db.session.add(new_game)
            db.session.add(user)
            db.session.commit()
            flash(f"{game_title} has been added to your library!", "success")

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
        "add-game.html",
        form=form,
        text="Add game",
        title="Game Progress | Add Game",
        btn_action="Add Game",
    )


@app.route("/library/")
@login_required
def library():
    user = User.query.filter_by(id=current_user.id).first()

    return render_template(
        "library.html",
        title="Game Progress | My Library",
        username=user.username,
        games=user.games,
    )


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete_game():
    if request.method == "POST":
        game_id = request.form.getlist("id")
        # print(game_id[0])
        game = db.session.get(Game, game_id[0])
        db.session.delete(game)
        db.session.commit()

        return url_for("library")


if __name__ == "__main__":
    app.run(debug=True)
