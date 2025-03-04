from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Access the database
db = client["dss_database"]

# Access the collection
signatures_collection = db["signatures"]

print("Connected to MongoDB successfully!")
