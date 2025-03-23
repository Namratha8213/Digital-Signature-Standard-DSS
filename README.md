# Digital Signature Standard (DSS)

## Overview

The **Digital Signature Standard (DSS)** is a cryptographic technique used for verifying the authenticity and integrity of digital messages or documents. This project implements DSS using Python and MongoDB for secure digital signature generation and verification.

## Features

- User authentication (Registration & Login)
- Digital signature generation
- Signature verification
- Secure database storage using MongoDB
- API-based interaction using Flask

## Technologies Used

- **Python** (Core language)
- **Flask** (For API endpoints)
- **Cryptography** (For cryptographic operations)
- **MongoDB** (For storing user credentials and signatures)
- **JWT** (For authentication & security)

## Project Structure

```
├── api.py                  # API endpoints (Flask-based)
├── database.py             # MongoDB database interactions
├── dss.py                  # Core DSS implementation (empty)
├── fetch_signatures.py     # Retrieve stored signatures
├── generate_signature.py   # Generate digital signatures
├── mongodb_connection.py   # MongoDB connection handler
├── register_user.py        # User registration
├── test_mongo.py          # MongoDB connection test
├── verify_signature.py     # Verify digital signatures
└── README.md              # Project documentation
```

## Installation & Setup

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7+**
- **MongoDB** (Running locally on default port 27017)
- **pip** (Python package manager)

### Required Python Packages

- flask
- flask-jwt-extended
- pymongo
- cryptography
- werkzeug
- PyJWT

### Steps to Run

1. **Clone the repository**
2. **Install the required packages:**
   ```sh
   pip install flask flask-jwt-extended pymongo cryptography werkzeug PyJWT
   ```
3. **Ensure MongoDB is running locally**
4. **Test MongoDB connection:**
   ```sh
   python test_mongo.py
   ```
5. **Run the Flask API:**
   ```sh
   python api.py
   ```

## API Endpoints

### User Registration

**POST /register**

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### User Login

**POST /login**

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### Generate Digital Signature

**POST /generate_signature**

```json
{
  "message": "Hello, this is a test!"
}
```

### Verify Signature

**POST /verify_signature**

```json
{
  "message": "Hello, this is a test!",
  "signature": "<signature_from_response>"
}
```

### Get User Signatures

**GET /get_signature**

- Requires JWT authentication token

## Security Features

- Password hashing using PBKDF2
- JWT-based authentication
- Signature expiration (24 hours by default)
- RSA-2048 key pairs for signatures
- PSS padding with SHA-256 for signature generation

## Future Enhancements

- Add proper error handling and logging
- Implement rate limiting
- Add user roles and permissions
- Create a web interface
- Add signature revocation capability

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

📌 **Note:** This project is for educational purposes and demonstrates basic DSS implementation.
