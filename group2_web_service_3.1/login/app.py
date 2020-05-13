from flask import Flask, request, abort, redirect, jsonify
import re
import jwt
import datetime
app = Flask(__name__)

JWT_TOKEN_SECRET = "Some_very_good_password_secret_like_thing_or_so"
urls = {'0':'https://www.google.com'}
users = {}

@app.route("/users", methods=["POST"])
def route_users():
    global users
    username = request.form["username"]
    password = request.form["password"]
    users[username] = password
    return ""


def generate_expiration_date():
    return datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

@app.route("/users/login", methods=["POST"])
def route_users_login():
    global users
    username = request.form["username"]
    password = request.form["password"]

    if username not in users or users[username] != password: 
        return "forbidden", 403
    
    data = {
        'username': username,
        'password': password,
        # Set the expiration date, library looks at this date 
        # and verifies it on decryption, no custom code required.
        "exp": generate_expiration_date()
    }
    return jsonify(jwt.encode(data, JWT_TOKEN_SECRET, algorithm='HS256').decode("utf-8"))


app.run(host='0.0.0.0', port='80')