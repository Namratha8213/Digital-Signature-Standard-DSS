from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from generate_signature import generate_and_store_signature
from verify_signature import verify_signature
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)

# Secret key for JWT authentication
app.config["JWT_SECRET_KEY"] = "your_secret_key_here"
jwt = JWTManager(app)


# Token expiration time
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Increases token validity to 1 hour

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
users_collection = db["users"]
signatures_collection = db["signatures"]  # ✅ Fix: Define signatures collection here

@app.route("/register", methods=["POST"])
def register():
    """Register a new user and store hashed password."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists!"}), 400

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully!"}), 201

@app.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Fetch user from MongoDB
    user = users_collection.find_one({"username": username})

    if user and check_password_hash(user["password"], password):
        token = create_access_token(identity=username)
        return jsonify({"token": token.decode('utf-8') if isinstance(token, bytes) else token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/generate_signature", methods=["POST"])
@jwt_required()
def generate_signature():
    """Generate and store digital signature for authenticated users."""
    username = get_jwt_identity()
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Call function to generate and store signature
    generate_and_store_signature(username, message)
    return jsonify({"message": "Signature generated successfully!"}), 201


@app.route("/verify_signature", methods=["POST"])
@jwt_required()
def verify_signature_api():
    """Verify digital signature for authenticated users."""
    username = get_jwt_identity()
    data = request.get_json()
    message = data.get("message")
    signature = data.get("signature")

    if not message or not signature:
        return jsonify({"error": "Message and signature are required!"}), 400

    verification_result = verify_signature(username, message, signature)
    return jsonify(verification_result)


@app.route("/get_signature", methods=["GET"])
@jwt_required()
def get_signature():
    """Retrieve all stored signatures for a logged-in user."""
    username = get_jwt_identity()

    # Fetch all signatures for the user
    user_doc = signatures_collection.find_one({"username": username}, {"_id": 0, "signatures": 1})

    if not user_doc or "signatures" not in user_doc:
        return jsonify({"error": "❌ No signatures found for this user."}), 404

    return jsonify({"signatures": user_doc["signatures"]})

if __name__ == "__main__":
    print(app.url_map)  # ✅ Print all registered routes
    app.run(debug=True)

