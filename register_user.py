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
    hashed_password = generate_password_hash(password)

    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return {"message": "User already exists!"}

    users_collection.insert_one({"username": username, "password": hashed_password})

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"message": "User registered successfully!", "token": token}

# Example Usage
print(register_user("test_user", "securepassword"))



# import bcrypt
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["dss_database"]
# users_collection = db["users"]

# def register_user(username, password):
#     # Check if the user already exists
#     if users_collection.find_one({"username": username}):
#         print("❌ Username already exists. Choose a different one.")
#         return
    
#     # Hash the password before storing it
#     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

#     # Store user in database
#     users_collection.insert_one({
#         "username": username,
#         "password": hashed_password
#     })

#     print("✅ User registered successfully!")

# # Example usage
# username = input("Enter a username: ")
# password = input("Enter a password: ")
# register_user(username, password)
