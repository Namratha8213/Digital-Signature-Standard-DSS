from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from pymongo import MongoClient
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64

app = Flask(__name__)
SECRET_KEY = "your_secret_key"

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
users_collection = db["users"]
signatures_collection = db["signatures"]

# ----------------- JWT Authentication Middleware -----------------
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            token = token.split(" ")[1]  # Remove "Bearer " prefix
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return wrapper

# ----------------- User Registration -----------------
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists!"}), 400

    users_collection.insert_one({"username": username, "password": password})

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"message": "User registered successfully!", "token": token})

# ----------------- User Login -----------------
@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username})
    if not user or user["password"] != password:
        return jsonify({"message": "Invalid credentials!"}), 401

    # Generate JWT token
    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"message": "Login successful!", "token": token})

# ----------------- Generate Digital Signature -----------------
@app.route("/generate_signature", methods=["POST"])
@token_required
def generate_signature():
    data = request.json
    message = data.get("message").encode()

    # Generate RSA key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Convert keys to PEM format for storage
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Sign the message
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Convert signature to base64 for storage
    signature_b64 = base64.b64encode(signature).decode("utf-8")

    # Store in MongoDB
    signatures_collection.insert_one({
        "message": data.get("message"),
        "signature": signature_b64,
        "public_key": public_pem.decode()
    })

    return jsonify({"message": "Signature generated and stored successfully!"})

# ----------------- Verify Digital Signature -----------------
@app.route("/verify_signature", methods=["POST"])
@token_required
def verify_signature():
    data = request.json
    message = data.get("message").encode()

    # Fetch stored signature
    signature_data = signatures_collection.find_one({"message": data.get("message")})
    if not signature_data:
        return jsonify({"message": "No matching signature found!"}), 404

    signature = base64.b64decode(signature_data["signature"])
    public_key_pem = signature_data["public_key"].encode()

    # Load the public key
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Verify the signature
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return jsonify({"message": "✅ Signature is valid!"})
    except Exception:
        return jsonify({"message": "❌ Signature verification failed!"})

if __name__ == "__main__":
    app.run(debug=True)
