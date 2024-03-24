from flask import Flask, request, render_template, redirect, url_for

# Flask constructor
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/add-game")
def add_games():
    return render_template("add-game.html")


# Route for handling the login page logic
@app.route("/test", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/library")
def library():
    return render_template("library.html")


# A decorator used to tell the application
# which URL is associated function
# @app.route("/test.py", methods=["GET", "POST"])
# def get_freq():
#     if request.method == "POST":
#         # getting input with freq = set_freq in HTML form
#         freq = request.form.get("set_freq")  # <--- do whatever you want with that value
#         return "Your freq value is " + freq
#     return render_template("add-game.html")


if __name__ == "__main__":
    app.run()
