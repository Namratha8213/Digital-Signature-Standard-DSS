import base64
import logging
from datetime import datetime
from pymongo import MongoClient
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

def verify_signature(username, message, signature):
    """Verify the signature for a given message and check expiration."""
    logging.info(f"Verifying signature for user: {username} - Message: {message}")

    # Fetch the correct stored signature for the given message
    user_doc = signatures_collection.find_one({"username": username})

    if not user_doc or "signatures" not in user_doc:
        logging.warning(f"No signatures found for user: {username}")
        return {"error": "❌ No signatures found for this user."}

    # Initialize variables to prevent UnboundLocalError
    stored_signature, public_key_pem, expires_at = None, None, None

    # Find the correct signature for the given message
    for sig in user_doc["signatures"]:
        if sig["message"] == message:
            stored_signature = base64.b64decode(sig["signature"])
            public_key_pem = sig["public_key"].encode()  # Ensure it's encoded
            expires_at = datetime.fromisoformat(sig["expires_at"])
            break  # ✅ Stop searching once we find a match

    if not stored_signature or not public_key_pem or not expires_at:
        logging.warning(f"No matching signature found for message: {message}")
        return {"error": "❌ No matching signature found for the given message."}

    # Check if the signature is expired (ensure both timestamps are UTC-aware)
    if datetime.utcnow().replace(tzinfo=None) > expires_at.replace(tzinfo=None):
        logging.warning("Signature has expired.")
        return {"error": "⏳ Signature has expired and cannot be verified."}

    # Load the public key safely
    try:
        public_key = serialization.load_pem_public_key(public_key_pem)
    except ValueError:
        logging.error("Invalid public key format.")
        return {"error": "⚠️ Invalid public key format."}

    # Verify the signature
    try:
        public_key.verify(
            stored_signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        logging.info("Signature verification successful!")
        return {"message": "✅ Signature is valid!"}
    
    except InvalidSignature:
        logging.warning("Signature verification failed: Invalid signature.")
        return {"error": "❌ Signature verification failed: Invalid signature."}
    
    except Exception as e:
        logging.error(f"Unexpected error during verification: {str(e)}")
        return {"error": f"⚠️ An unexpected error occurred: {str(e)}"}
