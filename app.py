from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "liamyork"
app.config["MYSQL_PASSWORD"] = "ldmmkr28102001"
app.config["MYSQL_DB"] = "pawpair"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["UPLOAD_FOLDER"] = "uploads"
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        # check if email already exists
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            return render_template("register_error.html", message="This email is already in use. Please use a different email address.")
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cur.close()
        return render_template("register_success.html", username=username)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            return f"Welcome, {user['username']}!"
        else:
            return "Invalid email or password. Please try again."
    return render_template("login.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        username = request.form["username"]
        profile_image = request.files["profile_image"]
        location = request.form["location"]  # use google api
        dog_name = request.form["dog_name"]
        breed = request.form["breed"]
        age = request.form["age"]
        description = request.form["description"]
        dog_image = request.files["dog_image"]
        profile_image_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(profile_image.filename))
        profile_image.save(profile_image_path)
        dog_image_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(dog_image.filename))
        dog_image.save(dog_image_path)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO profiles (username, profile_image, location, dog_name, breed, age, description, dog_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (username, profile_image_path, location, dog_name, breed, age, description, dog_image_path))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("dashboard"))
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)