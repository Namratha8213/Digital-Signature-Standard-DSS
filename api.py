from flask import Flask, request, jsonify
from auth_middleware import token_required
from generate_signature import generate_digital_signature
from verify_signature import verify_digital_signature

app = Flask(__name__)

@app.route("/generate_signature", methods=["POST"])
@token_required
def generate_signature():
    data = request.json
    message = data.get("message")
    if not message:
        return jsonify({"error": "Message is required!"}), 400
    signature = generate_digital_signature(message)
    return jsonify({"message": message, "signature": signature})

@app.route("/verify_signature", methods=["POST"])
@token_required
def verify_signature():
    data = request.json
    message = data.get("message")
    signature = data.get("signature")

    if not message or not signature:
        return jsonify({"error": "Message and signature are required!"}), 400

    is_valid = verify_digital_signature(message, signature)
    return jsonify({"is_valid": is_valid})
