import sqlite3

def get_user_by_username(username):
    """
    VULNERABLE: Concatenates user input directly into the SQL query.
    An attacker can input crafted strings to alter the query's behavior.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'" # Dangerous
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

# Attacker input example: admin' OR '1'='1 -- This could bypass authentication.
