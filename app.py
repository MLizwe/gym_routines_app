from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Folder for uploaded images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    routines = session.get("routines", [])
    return render_template("routines.html", routines=routines)

@app.route("/delete")
def delete():
    name = request.args.get("name")
    if name:
        routines = session.get("routines", [])
        routines = [r for r in routines if r["name"] != name]
        session["routines"] = routines
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        muscle_group = request.form["muscle_group"]
        difficulty = request.form["difficulty"]
        description = request.form["description"]
        image = request.files["image"]

        image_filename = ""
        if image and allowed_file(image.filename):
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Get existing routines or start new
        routines = session.get("routines", [])
        routines.append({
            "name": name,
            "muscle_group": muscle_group,
            "difficulty": difficulty,
            "description": description,
            "image": image_filename
        })

        session["routines"] = routines  # Save back to session

        return redirect(url_for("home"))

    return render_template("add.html")


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
