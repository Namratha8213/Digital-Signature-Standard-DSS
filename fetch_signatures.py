from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

# Fetch all signatures
signatures = signatures_collection.find()

# Display signatures
for signature in signatures:
    print(signature)
