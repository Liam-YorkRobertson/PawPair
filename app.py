from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
import requests
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)

app.config['SECRET_KEY'] = "70b838f5207221d256a941f20dff9da2"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "liamyork"
app.config["MYSQL_PASSWORD"] = "ldmmkr28102001"
app.config["MYSQL_DB"] = "pawpair"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)
UPLOAD_FOLDER = os.path.join("static", "images")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
user_profile_images_folder = "user_profile_images"
dog_profile_images_folder = "dog_profile_images"

socketio = SocketIO(app)
active_chatrooms = set()

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
            session['username'] = user['username']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user_profiles WHERE username = %s", (user['username'],))
            user_profile = cur.fetchone()
            cur.close()
            
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM breeder_profiles WHERE username = %s", (user['username'],))
            breeder_profile = cur.fetchone()
            cur.close()
            if user_profile:
                return redirect(url_for("user_dashboard"))
            elif breeder_profile:
                return redirect(url_for("breeder_dashboard"))
            else:
                return redirect(url_for("user_or_breeder"))
        else:
            return "Invalid email or password. Please try again."
    return render_template("login.html")

@app.route("/user_or_breeder")
def user_or_breeder():
    return render_template("user_or_breeder.html")

@app.route("/user_profile", methods=["GET", "POST"])
def user_profile():
    if request.method == "POST":
        username = request.form["username"]
        profile_image = request.files["profile_image"]
        location = request.form["location"]  # use Google API
        dog_name = request.form["dog_name"]
        breed = request.form["breed"]
        age = request.form["age"]
        description = request.form["description"]
        dog_image = request.files["dog_image"]
        profile_image_path = os.path.join(app.config["UPLOAD_FOLDER"], user_profile_images_folder, secure_filename(profile_image.filename))
        dog_image_path = os.path.join(app.config["UPLOAD_FOLDER"], dog_profile_images_folder, secure_filename(dog_image.filename))
        profile_image.save(profile_image_path)
        dog_image.save(dog_image_path)
        # Fetch the user's ID from the users table based on the username
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        user_id = user['id']
        # Check if the user already has a profile
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user_profiles WHERE user_id = %s", (user_id,))
        existing_profile = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        if existing_profile:
            cur.execute("UPDATE user_profiles SET profile_image=%s, location=%s, dog_name=%s, breed=%s, age=%s, description=%s, dog_image=%s WHERE user_id=%s",
                        (os.path.join(user_profile_images_folder, secure_filename(profile_image.filename)), location, dog_name, breed, age, description, os.path.join(dog_profile_images_folder, secure_filename(dog_image.filename)), user_id))
        else:
            cur.execute("INSERT INTO user_profiles (user_id, username, profile_image, location, dog_name, breed, age, description, dog_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, username, os.path.join(user_profile_images_folder, secure_filename(profile_image.filename)), location, dog_name, breed, age, description, os.path.join(dog_profile_images_folder, secure_filename(dog_image.filename))))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("user_dashboard")) 
    return render_template("user_profile.html")

def check_if_user_in_chatroom(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT 1 FROM messages WHERE sender_username = %s OR receiver_username = %s LIMIT 1", (username, username))
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists

@app.route("/user_dashboard")
def user_dashboard():
    is_in_chatroom = check_if_user_in_chatroom(session['username'])
    return render_template("user_dashboard.html", is_in_chatroom=is_in_chatroom)

@app.route("/fetch_dog_breeds", methods=["POST"])
def fetch_dog_breeds():
    search_query = request.form.get('search_query', '').lower()
    logged_in_username = session.get('username')
    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT breed FROM user_profiles WHERE username != %s AND breed LIKE %s ORDER BY breed LIMIT 10", (logged_in_username, f'%{search_query}%'))
    breeds = [row['breed'] for row in cur.fetchall()]
    cur.close()
    
    response_data = {
        "success": True,
        "breeds": breeds
    }
    return jsonify(response_data)

def fetch_random_user_profile(logged_in_username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_profiles WHERE username != %s ORDER BY RAND() LIMIT 1", (logged_in_username,))
    profile_data = cur.fetchone()
    cur.close()
    if profile_data:
        response_data = {
            "success": True,
            "profileData": {
                "profile_image": "/static/images/" + profile_data["profile_image"],
                "username": profile_data["username"],
                "location": profile_data["location"],
                "dog_name": profile_data["dog_name"],
                "breed": profile_data["breed"],
                "age": profile_data["age"],
                "description": profile_data["description"],
                "dog_image": "/static/images/" + profile_data["dog_image"]
            }
        }
    else:
        response_data = {
            "success": False,
            "error": "No user profiles found."
        }
    return jsonify(response_data)

@app.route("/fetch_random_user_profile")
def fetch_random_user_profile_route():
    logged_in_username = session.get('username')
    return fetch_random_user_profile(logged_in_username)

@app.route("/breeder_profile", methods=["GET", "POST"])
def breeder_profile():
    if request.method == "POST":
        username = request.form["username"]
        business_name = request.form["business_name"]
        location = request.form["location"]
        specialization = request.form["specialization"]
        contact_telephone = request.form["contact_telephone"]
        contact_email = request.form["contact_email"]
        profile_image = request.files["profile_image"]
        profile_image_path = os.path.join(app.config["UPLOAD_FOLDER"], "breeder_profile_images", secure_filename(profile_image.filename))
        profile_image.save(profile_image_path)
        # Fetch the user's ID from the users table based on the username
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        user_id = user['id']
        # Check if the user already has a breeder profile
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM breeder_profiles WHERE user_id = %s", (user_id,))
        existing_profile = cur.fetchone()
        cur.close()
        cur = mysql.connection.cursor()
        if existing_profile:
            cur.execute("UPDATE breeder_profiles SET business_name=%s, location=%s, specialization=%s, contact_telephone=%s, contact_email=%s, profile_image=%s WHERE user_id=%s",
                        (business_name, location, specialization, contact_telephone, contact_email, os.path.join("breeder_profile_images", secure_filename(profile_image.filename)), user_id))
        else:
            cur.execute("INSERT INTO breeder_profiles (user_id, username, business_name, location, specialization, contact_telephone, contact_email, profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, username, business_name, location, specialization, contact_telephone, contact_email, os.path.join("breeder_profile_images", secure_filename(profile_image.filename))))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("breeder_dashboard"))
    return render_template("breeder_profile.html")

@app.route("/breeder_dashboard")
def breeder_dashboard():
    return render_template("breeder_dashboard.html")

@app.route("/get_location")
def get_location():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key=AIzaSyBhgGTbERJQi_NKs2xS3iAxX303W3fQ6iY'
    response = requests.get(geocoding_url)
    data = response.json()
    if response.status_code == 200 and 'results' in data:
        for result in data['results']:
            for component in result['address_components']:
                if 'administrative_area_level_1' in component['types']:
                    province = component['long_name']
                elif 'country' in component['types']:
                    country = component['long_name']
                    break
        return jsonify(success=True, province=province, country=country)
    else:
        return jsonify(success=False, error='Failed to fetch location data')

@app.route("/search_users", methods=["GET"])
def search_users():
    breed = request.args.get("breed")
    logged_in_username = session.get('username')
    # Fetch user profiles based on the breed parameter
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_profiles WHERE breed = %s AND username != %s", (breed, logged_in_username))
    user_profiles = cur.fetchall()
    cur.close()
    return render_template("user_list.html", user_profiles=user_profiles, breed=breed)

@app.route("/get_chatroom_username", methods=["GET"])
def get_chatroom_username():
    logged_in_username = session.get('username')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT receiver_username, sender_username FROM messages WHERE receiver_username = %s OR sender_username = %s LIMIT 1", (logged_in_username, logged_in_username))
    chatroom_data = cursor.fetchone()
    cursor.close()

    if chatroom_data:
        if chatroom_data['receiver_username'] == logged_in_username:
            other_user = chatroom_data['sender_username']
        else:
            other_user = chatroom_data['receiver_username']

        response_data = {
            "success": True,
            "username": other_user
        }
    else:
        response_data = {
            "success": False,
            "error": "No chatroom found."
        }
    return jsonify(response_data)

def get_user_id(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result['id']
    else:
        return None

def get_breeder_profiles(location):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM breeder_profiles WHERE location = %s", (location,))
    breeder_profiles = cur.fetchall()

    # Convert the list of dictionaries to a list of tuples
    breeder_profiles_list = []
    for profile in breeder_profiles:
        breeder_profiles_list.append({
            'username': profile['username'],
            'business_name': profile['business_name'],
            'location': profile['location'],
            'specialization': profile['specialization'],
            'contact_telephone': profile['contact_telephone'],
            'contact_email': profile['contact_email'],
            'profile_image': profile['profile_image']
        })

    cur.close()
    return breeder_profiles_list
 
@app.route("/chatroom/<username>")
def chatroom(username):
    sender_username = session.get('username')
    # Check if there's an existing chatroom with the given sender and receiver usernames
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT chatroom_id FROM messages WHERE (sender_username = %s AND receiver_username = %s) OR (sender_username = %s AND receiver_username = %s) LIMIT 1", (sender_username, username, username, sender_username))
    existing_chatroom = cursor.fetchone()
    cursor.close()

    if existing_chatroom:
        chatroom_id = existing_chatroom['chatroom_id']
    else:
        # If no existing chatroom found, create a new chatroom_id
        chatroom_id = f"{sender_username}_{username}"

    # Fetch chat messages for the specific chatroom from the messages table
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM messages WHERE chatroom_id = %s", (chatroom_id,))
    messages = cursor.fetchall()
    cursor.close()
    
    # Get the location of the signed-in user from the user_profiles table
    signed_in_username = session.get('username')
    cur = mysql.connection.cursor()
    cur.execute("SELECT location FROM user_profiles WHERE username = %s", (signed_in_username,))
    signed_in_user_location = cur.fetchone().get('location')
    cur.close()

    # Fetch breeder profiles in the same location as the signed-in user
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM breeder_profiles WHERE location = %s", (signed_in_user_location,))
    breeder_profiles = cur.fetchall()
    cur.close()
    
    return render_template("chatroom.html", sender_username=signed_in_username, receiver_username=username, messages=messages, chatroom_id=chatroom_id, breeder_profiles=breeder_profiles)
    
@socketio.on("connectToUser")
def handle_connect_to_user(data):
    sender_username = session.get('username')
    receiver_username = data['username']
    session['receiver_username'] = receiver_username  # Store receiver's username in session
    room = f"{sender_username}_{receiver_username}"
    join_room(room)

@socketio.on("chatMessage")
def handle_chat_message(data):
    sender_username = session.get('username')  # Retrieve sender's username from the session
    receiver_username = data['receiver_username']
    
    # Check if there's an existing chatroom with the given sender and receiver usernames
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT chatroom_id FROM messages WHERE (sender_username = %s AND receiver_username = %s) OR (sender_username = %s AND receiver_username = %s) LIMIT 1", (sender_username, receiver_username, receiver_username, sender_username))
    existing_chatroom = cursor.fetchone()
    cursor.close()

    if existing_chatroom:
        chatroom_id = existing_chatroom['chatroom_id']
    else:
        # If no existing chatroom found, create a new chatroom_id
        chatroom_id = f"{sender_username}_{receiver_username}"

    sender_id = get_user_id(sender_username)
    receiver_id = get_user_id(receiver_username)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO messages (chatroom_id, sender_id, receiver_id, sender_username, receiver_username, message) VALUES (%s, %s, %s, %s, %s, %s)",
                   (chatroom_id, sender_id, receiver_id, sender_username, receiver_username, data['message']))
    mysql.connection.commit()
    cursor.close()

    room = f"{sender_username}_{receiver_username}"
    emit("chatMessage", {"sender": sender_username, "message": data['message']}, room=room)

@app.route('/terminate_chatroom', methods=['DELETE'])
def terminate_chatroom():
    sender_username = session.get('username')
    receiver_username = request.args.get('receiver_username')

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM messages WHERE ((sender_username = %s AND receiver_username = %s) OR (sender_username = %s AND receiver_username = %s))",
                   (sender_username, receiver_username, receiver_username, sender_username))
    mysql.connection.commit()
    cursor.close()

    return jsonify(success=True), 200

@app.route('/user_thank_you')
def user_thank_you():
    return render_template('user_thank_you.html')

if __name__ == "__main__":
    socketio.run(app, debug=True)