"""
Vulnerable Flask Application
This application contains intentional security vulnerabilities for testing purposes.
"""

import subprocess
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Vulnerability 1: SQL Injection
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # VULNERABLE: SQL Injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

# Vulnerability 2: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # VULNERABLE: Command Injection
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return result.stdout

# Vulnerability 3: Server-Side Template Injection (SSTI)
@app.route('/greet')
def greet():
    name = request.args.get('name', 'World')
    # VULNERABLE: SSTI
    template = f"<h1>Hello, {name}!</h1>"
    return render_template_string(template)

# Vulnerability 4: Hardcoded Credentials
DATABASE_PASSWORD = "admin123"  # VULNERABLE: Hardcoded secret
API_KEY = "sk-1234567890abcdef"  # VULNERABLE: Exposed API key

# Vulnerability 5: Insecure Deserialization
import pickle
import base64

@app.route('/load')
def load_data():
    data = request.args.get('data', '')
    # VULNERABLE: Insecure Deserialization
    obj = pickle.loads(base64.b64decode(data))
    return str(obj)

if __name__ == '__main__':
    app.run(debug=True)  # VULNERABLE: Debug mode in production
