from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from pymongo import MongoClient
import base64

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

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

# Sign a message
message = b"Hello, this is a digitally signed message!"
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Convert signature to base64 for storage
signature_b64 = base64.b64encode(signature).decode('utf-8')

# Store in MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["dss_database"]
signatures_collection = db["signatures"]

signatures_collection.insert_one({
    "message": message.decode(),
    "signature": signature_b64,
    "public_key": public_pem.decode()
})

print("Signature stored in MongoDB successfully!")
