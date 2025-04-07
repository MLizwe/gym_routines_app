from flask import Flask, render_template, request, redirect, url_for
import os,csv

app = Flask(__name__)

# Sample data (temporary in-memory list)
routines = [
    {"name": "Chest Day", "exercises": ["Bench Press", "Push Ups", "Cable Fly"], "image": "chest.jpg"},
    {"name": "Leg Day", "exercises": ["Squats", "Lunges", "Leg Press"], "image": "legs.jpg"}
]

# Folder for uploaded images
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Check if uploaded file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    routines = []

    if os.path.exists("routines.csv"):
        with open ("routines.csv", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 5:
                    routines.append({
                        "name": row[0],
                        "muscle_group": row[1],
                        "difficulty": row[2],
                        "description": row[3],
                        "image": row[4]
                    })

    return render_template("routines.html", routines=routines)




@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        muscle_group = request.form["muscle_group"]
        difficulty = request.form["difficulty"]
        description = request.form["description"]
        image = request.files["image"]

        image_filename = ""
        if image:
            image_filename = image.filename
            image.save(os.path.join("static/uploads", image_filename))

        with open("routines.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, muscle_group, difficulty, description, image_filename])

        return redirect(url_for("home"))

    return render_template("add.html")


if __name__ == "__main__":
    # Make sure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
