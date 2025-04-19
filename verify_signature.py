from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from pymongo import MongoClient
from datetime import datetime, timezone
import base64

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

def verify_signature(username, message, signature):
    """Verify the digital signature for a given message."""

    # Fetch user's stored signatures
    user_doc = signatures_collection.find_one({"username": username})
    if not user_doc or "signatures" not in user_doc:
        return {"valid": False, "error": "❌ No signatures found for this user."}

    # Match message
    matching_entry = next(
        (s for s in user_doc["signatures"] if s["message"] == message),
        None
    )
    if not matching_entry:
        return {"valid": False, "error": "❌ No matching message found."}

    # Decode signature and public key
    try:
        stored_signature = base64.b64decode(matching_entry["signature"])
        public_key_pem = matching_entry["public_key"].encode()
        expires_at = datetime.fromisoformat(matching_entry["expires_at"]).replace(tzinfo=timezone.utc)
    except Exception as e:
        return {"valid": False, "error": f"❌ Error parsing stored data: {str(e)}"}

    # Check expiration
    if datetime.now(timezone.utc) > expires_at:
        return {"valid": False, "error": "⏳ Signature has expired."}

    # Load public key and verify
    try:
        public_key = serialization.load_pem_public_key(public_key_pem)
        public_key.verify(
            stored_signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return {"valid": True}
    except Exception as e:
        return {"valid": False, "error": f"❌ Signature verification failed: {str(e)}"}

# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes, serialization
# from pymongo import MongoClient
# import base64
# from datetime import datetime

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["dss_database"]
# signatures_collection = db["signatures"]

# def verify_signature(username, message, signature):
#     """Verify the signature for a given message and check expiration."""

#     # Fetch the correct stored signature for the given message
#     user_doc = signatures_collection.find_one({"username": username})

#     if not user_doc or "signatures" not in user_doc:
#         return {"error": "❌ No signatures found for this user."}

#     for sig in user_doc["signatures"]:
#         if sig["message"] == message:
#             stored_signature = base64.b64decode(sig["signature"])
#             public_key_pem = sig["public_key"].encode()
#             expires_at = datetime.fromisoformat(sig["expires_at"])
#             break
#     else:
#         return {"error": "❌ No matching signature found for the given message."}

#     # Check if the signature is expired
#     if datetime.utcnow() > expires_at:
#         return {"error": "⏳ Signature has expired and cannot be verified."}

#     # Load the public key
#     public_key = serialization.load_pem_public_key(public_key_pem)

#     # Verify the signature
#     try:
#         public_key.verify(
#             stored_signature,
#             message.encode(),
#             padding.PSS(
#                 mgf=padding.MGF1(hashes.SHA256()),
#                 salt_length=padding.PSS.MAX_LENGTH
#             ),
#             hashes.SHA256()
#         )
#         return {"message": "✅ Signature is valid!"}
#     except Exception as e:
#         return {"error": f"❌ Signature verification failed: {str(e)}"}