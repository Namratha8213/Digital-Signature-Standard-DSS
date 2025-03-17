from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from pymongo import MongoClient
import base64

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

def verify_signature(username, message, signature):
    """Verify the signature for a given message."""
    
    # Fetch the correct stored signature for the given message
    user_doc = signatures_collection.find_one({"username": username})
    
    if not user_doc or "signatures" not in user_doc:
        return {"error": "❌ No signatures found for this user."}

    # Find the signature that matches the message
    for sig in user_doc["signatures"]:
        if sig["message"] == message:
            stored_signature = base64.b64decode(sig["signature"])
            public_key_pem = sig["public_key"].encode()
            break
    else:
        return {"error": "❌ No matching signature found for the given message."}

    # Load the public key
    public_key = serialization.load_pem_public_key(public_key_pem)

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
        return {"message": "✅ Signature is valid!"}
    except Exception as e:
        return {"error": f"❌ Signature verification failed: {str(e)}"}
