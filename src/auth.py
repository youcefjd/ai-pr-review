"""Authentication module with intentional security issues for testing."""

import sqlite3
from flask import request, jsonify


def login():
    """Handle user login - HAS SQL INJECTION VULNERABILITY."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # VULNERABILITY: SQL Injection - using f-string with user input
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    
    if user:
        # VULNERABILITY: Hardcoded secret key
        token = generate_token(username, secret_key="hardcoded_secret_123")
        return jsonify({"token": token})
    
    return jsonify({"error": "Invalid credentials"}), 401


def generate_token(username, secret_key):
    """Generate auth token."""
    import jwt
    return jwt.encode({"user": username}, secret_key, algorithm="HS256")


def get_user_data():
    """Get user data - HAS INFORMATION DISCLOSURE."""
    user_id = request.args.get('id')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: SQL Injection via query parameter
    query = f"SELECT * FROM users WHERE id={user_id}"
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        return jsonify(user)
    except Exception as e:
        # VULNERABILITY: Exposing internal error details
        return jsonify({
            "error": str(e),
            "query": query,  # Leaking internal query structure!
            "stack_trace": traceback.format_exc()
        }), 500
