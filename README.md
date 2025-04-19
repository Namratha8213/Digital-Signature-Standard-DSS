# Digital Signature Standard (DSS)

## Overview

The **Digital Signature Standard (DSS)** is a cryptographic technique used for verifying the authenticity and integrity of digital messages or documents. This project implements DSS using Python and MongoDB for secure digital signature generation and verification, with a React-based frontend interface.

## Features

- User authentication (Registration & Login)
- Digital signature generation
- Signature verification
- Secure database storage using MongoDB
- RESTful API using Flask
- React-based web interface
- Real-time signature status updates
- Signature expiration tracking

## Technologies Used

### Backend

- **Python** (Core language)
- **Flask** (For API endpoints)
- **Cryptography** (For cryptographic operations)
- **MongoDB** (For storing user credentials and signatures)
- **JWT** (For authentication & security)

### Frontend

- **React** (UI framework)
- **Axios** (HTTP client)
- **React Router** (Navigation)

## Project Structure

```
├── Backend
│   ├── api.py                  # API endpoints (Flask-based)
│   ├── database.py             # MongoDB database interactions
│   ├── generate_signature.py   # Generate digital signatures
│   ├── verify_signature.py     # Verify digital signatures
│   ├── register_user.py        # User registration
│   └── requirements.txt        # Python dependencies
│
├── dss-frontend               # React Frontend
│   ├── public/                # Static files
│   ├── src/
│   │   ├── pages/            # React components
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   └── Dashboard.js
│   │   ├── App.js            # Main React component
│   │   └── api.js            # API configuration
│   └── package.json          # Frontend dependencies
```

## Installation & Setup

### Prerequisites

- **Python 3.7+**
- **MongoDB** (Running locally on port 27017)
- **Node.js** and **npm**
- **pip** (Python package manager)

### Backend Setup

1. **Install Python packages:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Start MongoDB locally**
3. **Run the Flask API:**
   ```sh
   python api.py
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```sh
   cd dss-frontend
   ```
2. **Install dependencies:**
   ```sh
   npm install
   ```
3. **Start development server:**
   ```sh
   npm start
   ```

## Usage

1. Access the web interface at `http://localhost:3000`
2. Register a new account or login
3. Use the dashboard to:
   - Generate new signatures
   - View stored signatures
   - Verify existing signatures
   - Check signature expiration status

## API Endpoints

### Authentication

- **POST /register** - Create new user account
- **POST /login** - User authentication

### Signatures

- **POST /generate_signature** - Create new signature
- **POST /verify_signature** - Verify existing signature
- **GET /get_signature** - Retrieve user's signatures

## Security Features

- Password hashing using PBKDF2
- JWT-based authentication
- Signature expiration (24 hours by default)
- RSA-2048 key pairs for signatures
- PSS padding with SHA-256 for signature generation
- CORS protection
- Frontend token management

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

📌 **Note:** This project is for educational purposes and demonstrates basic DSS implementation.
