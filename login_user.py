import jwt
import datetime
from flask import Flask, request, jsonify
from database import get_user  # Assuming you have a function to fetch user data
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Secret key for encoding JWT
SECRET_KEY = "your_secret_key"
app.config["SECRET_KEY"] = SECRET_KEY

def generate_jwt(username):
    """Generate JWT Token"""
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = get_user(username)
    if user and bcrypt.check_password_hash(user["password"], password):
        token = generate_jwt(username)
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
