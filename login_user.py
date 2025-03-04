import bcrypt
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
users_collection = db["users"]

def login_user(username, password):
    user = users_collection.find_one({"username": username})

    if user and bcrypt.checkpw(password.encode(), user["password"]):
        print("✅ Login successful!")
        return True
    else:
        print("❌ Invalid username or password.")
        return False

# Example usage
username = input("Enter your username: ")
password = input("Enter your password: ")
login_user(username, password)
