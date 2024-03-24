from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route("/test.py", methods=["GET", "POST"])
def get_freq():
    if request.method == "POST":
        # getting input with freq = set_freq in HTML form
        game_title = request.form.get("game_title")
        game_progress = request.form.get("game_progress")
        return f"Your progress in {game_title} is {game_progress}"
    return render_template("add-game.html")


if __name__ == "__main__":
    app.run()
