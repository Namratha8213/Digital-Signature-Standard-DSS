from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from pymongo import MongoClient
import base64
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

def generate_and_store_signature(username, message, expiration_hours=24):
    """Generate a digital signature, store it, and set an expiration time."""
    
    # Generate RSA Key Pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Sign the message
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Convert signature and public key to a storable format
    signature_b64 = base64.b64encode(signature).decode()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

    expiration_time = datetime.utcnow() + timedelta(hours=expiration_hours)

    # Store in MongoDB
    signatures_collection.update_one(
        {"username": username},
        {"$push": {
            "signatures": {
                "message": message,
                "signature": signature_b64,
                "public_key": public_key_pem,
                "timestamp": datetime.utcnow().isoformat(),
                "expires_at": expiration_time.isoformat()  # Store expiration time
            }
        }},
        upsert=True
    )

    return {
        "message": "✅ Signature generated successfully!",
        "expires_at": expiration_time.isoformat()
    }
