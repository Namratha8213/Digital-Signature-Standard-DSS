from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
collection = db["signatures"]
