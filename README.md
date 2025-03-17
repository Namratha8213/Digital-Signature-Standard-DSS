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
- **PyCryptodome** (For cryptographic operations)
- **MongoDB** (For storing user credentials and signatures)
- **JWT** (For authentication & security)

## Project Structure

```
├── api.py                  # API endpoints (Flask-based)
├── database.py             # MongoDB database interactions
├── dss.py                  # Core Digital Signature Standard implementation
├── fetch_signatures.py     # Retrieve stored signatures
├── generate_signature.py   # Generate digital signatures
├── login_user.py           # User authentication
├── mongodb_connection.py   # MongoDB connection handler
├── register_user.py        # User registration
├── verify_signature.py     # Verify digital signatures
├── requirements.txt        # Python dependencies
├── .gitignore              # Ignore unnecessary files
└── README.md               # Project documentation
```

## Installation & Setup

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7+**
- **MongoDB** (Locally or via MongoDB Atlas)
- **pip** (Python package manager)

### Steps to Run

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Namratha8213/Digital-Signature-Standard-DSS.git
   cd Digital-Signature-Standard-DSS
   ```
2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up MongoDB:**

   - Run MongoDB locally or configure MongoDB Atlas.
   - Update the MongoDB URI in `mongodb_connection.py`.

5. **Run the Flask API:**
   ```sh
   python api.py
   ```
6. **Access the API:**
   Open `http://127.0.0.1:5000/` in your browser or use Postman to test endpoints.

## Usage

### User Registration

**Endpoint:** `POST /register`

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### User Login

**Endpoint:** `POST /login`

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### Generate Digital Signature

**Endpoint:** `POST /generate_signature`

```json
{
  "message": "Hello, this is a test!"
}
```

### Verify Signature

**Endpoint:** `POST /verify_signature`

```json
{
  "message": "Hello, this is a test!",
  "signature": "<signature_from_response>"
}
```

## Future Enhancements

- Implement a React-based UI for better user experience
- Deploy on cloud platforms (AWS, Render, Railway, etc.)
- Improve security with role-based authentication

## Contributing

Contributions are welcome! Feel free to fork the repo, submit issues, or create pull requests.

## License

This project is licensed under the MIT License.

---

📌 **Developed by [Namratha8213](https://github.com/Namratha8213)** 🚀
