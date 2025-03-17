from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from pymongo import MongoClient
import base64

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

def verify_signature(username):
    """Verify the signature for a logged-in user."""
    # Fetch the latest stored signature
    signature_data = signatures_collection.find_one({"username": username}, sort=[("_id", -1)])

    if signature_data:
        message = signature_data["message"].encode()
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
            return {"message": "✅ Signature is valid!"}
        except Exception as e:
            return {"error": f"❌ Signature verification failed: {str(e)}"}
    else:
        return {"error": "❌ No signatures found for this user."}
