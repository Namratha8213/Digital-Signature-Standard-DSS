import jwt
import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

SECRET_KEY = "your_secret_key"

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
users_collection = db["users"]

def register_user(username, password):
    """Registers a new user with a hashed password."""
    hashed_password = generate_password_hash(password)

    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return {"error": "User already exists!"}

    users_collection.insert_one({"username": username, "password": hashed_password})

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"message": "User registered successfully!", "token": token}

# Example Usage (for testing)
if __name__ == "__main__":
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    print(register_user(username, password))
