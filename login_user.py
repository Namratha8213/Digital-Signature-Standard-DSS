import jwt
import datetime
from pymongo import MongoClient
from werkzeug.security import check_password_hash

SECRET_KEY = "your_secret_key"

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
users_collection = db["users"]

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if not user or not check_password_hash(user["password"], password):
        return {"message": "Invalid credentials!"}

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"message": "Login successful!", "token": token}

# Example Usage
print(login_user("test_user", "securepassword"))


# import bcrypt
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["dss_database"]
# users_collection = db["users"]

# def login_user(username, password):
#     user = users_collection.find_one({"username": username})

#     if user and bcrypt.checkpw(password.encode(), user["password"]):
#         print("✅ Login successful!")
#         return True
#     else:
#         print("❌ Invalid username or password.")
#         return False

# # Example usage
# username = input("Enter your username: ")
# password = input("Enter your password: ")
# login_user(username, password)
