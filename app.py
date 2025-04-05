from flask import Flask, render_template, session
from flask_session import Session
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

file_save_location = "static/images"


@app.route("/add")
def add():
    # Logic for the 'add' route goes here
    return render_template("index.html")  # Or whatever page you want to render

@app.route("/")
def index():
    if "routines" not in session:
        session["routines"] = []

    return render_template("index.html", routines=session["routines"], file_location=file_save_location)

if __name__ == "__main__":
    app.run(debug=True)
