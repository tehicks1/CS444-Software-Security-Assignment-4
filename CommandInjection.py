import os
import sqlite3
import pickle
import hashlib
from flask import Flask, request

app = Flask(__name__)

# 🔑 Hardcoded secret
SECRET_KEY = "supersecret123"

# --- Vulnerability 1: Command Injection ---
@app.route("/ping")
def ping():
    # User input directly passed to shell command
    ip = request.args.get("ip", "")
    os.system(f"ping -c 1 {ip}")  # ❌ Command injection risk
    return f"Pinging {ip}"

# --- Vulnerability 2: SQL Injection ---
@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ❌ Unsafe string formatting for SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    result = cursor.fetchall()
    return str(result)

# --- Vulnerability 3: Insecure Deserialization ---
@app.route("/load")
def load():
    data = request.args.get("data", "")
    # ❌ Unpickling untrusted input
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

# --- Vulnerability 4: Use of eval ---
@app.route("/math")
def math():
    expr = request.args.get("expr", "1+1")
    # ❌ Dangerous evaluation of user input
    return str(eval(expr))

# --- Vulnerability 5: Weak Hash Algorithm ---
@app.route("/hash")
def hash_password():
    password = request.args.get("password", "default")
    # ❌ MD5 is cryptographically broken
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed

if __name__ == "__main__":
    app.run(debug=True)
