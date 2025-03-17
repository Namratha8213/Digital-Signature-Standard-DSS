from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from generate_signature import generate_and_store_signature
from verify_signature import verify_signature

app = Flask(__name__)

# Secret key for JWT authentication
app.config["JWT_SECRET_KEY"] = "your_secret_key_here"
jwt = JWTManager(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
users_collection = db["users"]

@app.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Fetch user from MongoDB
    user = users_collection.find_one({"username": username})

    if user and check_password_hash(user["password"], password):  # Check hashed password
        token = create_access_token(identity=username)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/generate_signature", methods=["POST"])
@jwt_required()  # Requires JWT token
def generate_signature():
    """Generate and store digital signature for authenticated users."""
    username = get_jwt_identity()  # Get logged-in user
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    generate_and_store_signature(username, message)
    return jsonify({"message": "Signature generated successfully!"}), 201

@app.route("/verify_signature", methods=["POST"])
@jwt_required()
def verify_signature_api():
    """Verify digital signature for authenticated users."""
    username = get_jwt_identity()
    verification_result = verify_signature(username)
    return jsonify(verification_result)

if __name__ == "__main__":
    app.run(debug=True)
