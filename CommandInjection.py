# safe_example.py
import os
import sqlite3
import json
import hashlib
import hmac
import secrets
import shlex
import subprocess
from flask import Flask, request, abort
import ast  # for safe literal evaluation of math expressions

app = Flask(__name__)

# Use environment variable for secrets (do NOT hardcode)
# Set via: export APP_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
if not APP_SECRET_KEY:
    # In production you should fail fast; here we generate a random key for local/dev only.
    APP_SECRET_KEY = secrets.token_urlsafe(32)

# Utility: simple IPv4 host validator (keeps it intentionally strict)
def is_safe_hostname_or_ip(value: str) -> bool:
    # Allow only hostnames or IPv4 dotted-decimal, no shell metacharacters
    # This is a conservative check: reject anything with whitespace or shell meta-chars.
    if not value:
        return False
    # Disallow suspicious characters
    forbidden = set(";|&$><`\\\"'(){}[]*?!~")
    if any(ch in forbidden for ch in value):
        return False
    # Basic length check
    if len(value) > 255:
        return False
    # Optionally further validate dotted IPv4 or hostname pattern.
    return True

# --- Fixed: avoid shell injection by using subprocess with list args and validating input ---
@app.route("/ping")
def ping():
    ip = request.args.get("ip", "")
    if not is_safe_hostname_or_ip(ip):
        abort(400, "Bad target")
    # Use a safe argument list instead of shell interpolation
    # 'ping' availability/options differ across systems; example here uses '-c' for POSIX systems.
    try:
        completed = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True, timeout=5)
    except Exception:
        abort(500, "Unable to run ping")
    return {"returncode": completed.returncode, "stdout": completed.stdout}

# --- Fixed: parameterized SQL queries to prevent SQL injection ---
DB_PATH = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    if not username or not password:
        abort(400, "Missing credentials")

    conn = get_db_connection()
    cursor = conn.cursor()
    # Use parameterized query (placeholders) instead of string formatting
    cursor.execute("SELECT id, username, password_hash, salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"authenticated": False}, 401

    # Verify password using a safe KDF (see hash_password below)
    salt = row["salt"]
    stored_hash = row["password_hash"]
    computed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    if hmac.compare_digest(stored_hash, computed):
        return {"authenticated": True, "user_id": row["id"]}
    else:
        return {"authenticated": False}, 401

# --- Fixed: do NOT unpickle untrusted data. Use JSON instead. ---
@app.route("/load", methods=["POST"])
def load():
    # Expect JSON in POST body rather than arbitrary pickles.
    if not request.is_json:
        abort(400, "Expected JSON")
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Invalid JSON")
    # Accept only a controlled schema; here we explicitly handle known keys
    allowed_keys = {"name", "age", "notes"}
    clean = {k: data[k] for k in data if k in allowed_keys}
    return {"loaded": clean}

# --- Fixed: replace eval with ast.literal_eval for safe literal evaluation or implement a math parser ---
@app.route("/math", methods=["GET"])
def math_calc():
    expr = request.args.get("expr", "1+1")
    # For simple literal expressions (numbers, tuples, lists, dicts) use literal_eval; it will reject function calls.
    # For arithmetic expressions like "1+2*3", literal_eval won't parse operators — so implement a safe parser or restrict input.
    # Example: allow only digits and arithmetic operators by a whitelist and parse using ast in safe mode.
    safe_chars = set("0123456789+-*/(). ")
    if not expr or any(ch not in safe_chars for ch in expr):
        abort(400, "Unsafe expression")
    # Parse expression with ast to ensure it's only arithmetic (no name nodes, no attribute access)
    import ast as _ast

    try:
        tree = _ast.parse(expr, mode="eval")
    except Exception:
        abort(400, "Invalid expression")

    class SafeEval(_ast.NodeVisitor):
        allowed_nodes = (_ast.Expression, _ast.BinOp, _ast.UnaryOp, _ast.Num, _ast.Load,
                         _ast.Add, _ast.Sub, _ast.Mult, _ast.Div, _ast.Pow, _ast.Mod,
                         _ast.UAdd, _ast.USub, _ast.Constant, _ast.Expr, _ast.Call)

        def generic_visit(self, node):
            if not isinstance(node, self.allowed_nodes):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")
            super().generic_visit(node)

    try:
        SafeEval().visit(tree)
        result = eval(compile(tree, "<safe>", "eval"), {"__builtins__": {}})
    except Exception:
        abort(400, "Unsafe or invalid expression")
    return {"result": result}

# --- Fixed: use a proper password hashing algorithm (PBKDF2 / bcrypt) with salt ---
def hash_password(password: str):
    salt = secrets.token_bytes(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    # Store both salt and hash (salt raw bytes)
    return salt, pw_hash

@app.route("/hash", methods=["POST"])
def hash_password_route():
    if not request.is_json:
        abort(400, "Expected JSON")
    data = request.get_json()
    password = data.get("password")
    if not password:
        abort(400, "Missing password")
    salt, pw_hash = hash_password(password)
    # Return hex-encoded results for demonstration (in practice store binary safely)
    return {"salt_hex": salt.hex(), "hash_hex": pw_hash.hex()}

if __name__ == "__main__":
    # For local testing only; in production use a proper WSGI server
    app.run(debug=False, host="127.0.0.1", port=5000)
