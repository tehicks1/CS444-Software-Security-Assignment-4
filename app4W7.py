# app.py
# Small, beginner-friendly demo that intentionally contains four separate insecure lines
# (for testing static analyzers like CodeQL).
#
# Each vulnerability is on its own line so tools will more clearly flag them.

import sqlite3
import pickle
import subprocess
import os

# ------------------------------
# 1) Hard-coded secret (single line)
# ------------------------------
DB_PASSWORD = "supersecretpassword123"  # <-- insecure: hard-coded credential on this line

# ------------------------------
# 2) SQL injection (single line)
# ------------------------------
def get_user_by_name(conn, username):
    # The following single line both builds and runs the query using string formatting.
    # If `username` is untrusted it can change the SQL meaning (SQL injection).
    return conn.execute("SELECT id, username FROM users WHERE username = '%s';" % username).fetchall()  # <-- insecure SQL construction & execution on this line

# ------------------------------
# 3) Insecure deserialization (single line)
# ------------------------------
def load_user_profile(serialized_bytes):
    # Using pickle.loads on data that might come from outside is dangerous.
    # This single line performs the unsafe deserialization.
    profile = pickle.loads(serialized_bytes)  # <-- insecure deserialization on this line
    return profile

# ------------------------------
# 4) Command injection (single line)
# ------------------------------
def list_files(directory):
    # This single line interpolates user input into a shell command and runs it with shell=True.
    # If `directory` contains unexpected characters, it can cause execution of other commands.
    output = subprocess.check_output(f"ls -la {directory}", shell=True, text=True)  # <-- insecure command invocation on this line
    return output

# ------------------------------
# Small safe demo (uses safe, local values)
# ------------------------------
if __name__ == "__main__":
    # Create a simple in-memory SQLite DB so example runs without setup
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT);")
    conn.execute("INSERT INTO users (username) VALUES ('alice');")
    conn.commit()

    # Safe demo use: we pass a literal (not user-supplied) so the demo won't be exploited here.
    print("Querying for 'alice':", get_user_by_name(conn, "alice"))

    # Demonstrate pickle usage with data produced in-process (still a bad pattern in general)
    serialized = pickle.dumps({"name": "charlie"})
    print("Loaded profile (from internal data):", load_user_profile(serialized))

    # Demonstrate listing a directory safely for the demo (still insecure pattern if directory was external)
    try:
        print("Files in /tmp (demo):")
        print(list_files("/tmp"))
    except Exception as e:
        print("list_files failed:", e)
