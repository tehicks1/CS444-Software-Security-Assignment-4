# app_flagged.py
# Intentionally insecure examples made explicit for static analysis testing.
# Each insecure API call is on its own line and reads from an obvious untrusted source.

import sqlite3
import pickle
import subprocess
import os
import sys

# ------------------------------
# 1) Hard-coded secret (single line)
# ------------------------------
# Many secret detectors look for names like "AWS_SECRET" or "API_KEY".
AWS_SECRET_ACCESS_KEY = "AKIAEXAMPLEKEY1234567890"  # <-- hard-coded credential (insecure)

# ------------------------------
# 2) SQL injection (single line)
# ------------------------------
def sql_injection_demo():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT);")
    conn.execute("INSERT INTO users (username) VALUES ('alice');")
    conn.commit()

    # Untrusted source: read a username from standard input (user-supplied)
    username = input("Enter username to find: ")  # source of untrusted data

    # Dangerous single-line SQL construction & execution using string formatting:
    # If username is something like "alice' OR '1'='1", this changes the query meaning.
    result = conn.execute("SELECT id, username FROM users WHERE username = '%s';" % username).fetchall()  # <-- insecure SQL on this line
    print("Query result:", result)

# ------------------------------
# 3) Insecure deserialization (single line)
# ------------------------------
def insecure_deserialize_demo():
    # Untrusted source: read raw data from an environment variable (could be attacker-controlled)
    raw = os.environ.get("UNTRUSTED_PROFILE_BYTES", "")  # source

    # Dangerous single-line deserialization of potentially untrusted bytes using pickle:
    profile = pickle.loads(raw.encode("utf-8"))  # <-- insecure deserialization on this line
    print("Loaded profile:", profile)

# ------------------------------
# 4) Command injection (single line)
# ------------------------------
def command_injection_demo():
    # Untrusted source: argument from the user (e.g., sys.argv)
    if len(sys.argv) > 1:
        directory = sys.argv[1]  # source
    else:
        directory = "/tmp"

    # Dangerous single-line shell invocation that interpolates untrusted input:
    output = subprocess.check_output(f"ls -la {directory}", shell=True, text=True)  # <-- insecure shell call on this line
    print(output)

# ------------------------------
# Demo runner (calls the functions)
# ------------------------------
if __name__ == "__main__":
    print("1) Hard-coded secret is present in AWS_SECRET_ACCESS_KEY (line near top).")
    print("2) SQL injection demo: provide input when prompted (or press Enter to skip).")
    try:
        sql_injection_demo()
    except Exception as e:
        print("SQL demo error:", e)

    print("\n3) Insecure deserialization demo: set environment variable UNTRUSTED_PROFILE_BYTES to something (or it will be empty).")
    try:
        insecure_deserialize_demo()
    except Exception as e:
        print("Deserialization demo error:", e)

    print("\n4) Command injection demo: pass a directory as the first argument, or it defaults to /tmp.")
    try:
        command_injection_demo()
    except Exception as e:
        print("Command demo error:", e)
