from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from pymongo import MongoClient
import base64

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

def generate_and_store_signature(username, message):
    """Generate a digital signature for an authenticated user."""

    # Generate RSA Key Pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Convert keys to PEM format
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
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Convert signature to base64 for storage
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    # Store in MongoDB
    signatures_collection.insert_one({
        "username": username,
        "message": message,
        "signature": signature_b64,
        "public_key": public_pem.decode()
    })

    print(f"✅ Signature stored successfully for user: {username}")

# Test run (for debugging)
if __name__ == "__main__":
    username = input("Enter your username: ")
    message = input("Enter the message to sign: ")
    generate_and_store_signature(username, message)
