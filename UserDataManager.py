import os
import pickle

# --- SECURITY VULNERABILITIES DEMONSTRATED ---
# 1. Command Injection (via os.system)
# 2. Insecure Deserialization (via pickle)
# 3. Directory Traversal/File Access Issues (via direct user input for file paths)

def search_user(username):
    """Vulnerability 1: Command Injection via os.system and lack of input validation."""
    print(f"\nSearching for user: {username}")
    # Insecure: Directly embedding user input into a shell command
    command = f"echo Listing files related to {username} in the current directory."
    print(f"Executing command: {command}")
    os.system(command) # Attacker can inject additional commands here (e.g., "; cat /etc/passwd")

def save_data(filename, data):
    """Vulnerability 2 & 3: Insecure Deserialization and Directory Traversal."""
    print(f"\nAttempting to save data to file: {filename}")
    try:
        # Vulnerability 3: Directory Traversal
        # An attacker can use paths like '../../../../etc/malicious.txt' to access restricted areas
        with open(filename, 'wb') as f:
            # Vulnerability 2: Insecure Deserialization
            # pickle.loads can execute arbitrary Python code if the input is malicious
            serialized_data = pickle.dumps(data)
            f.write(serialized_data)
        print("Data saved successfully (but insecurely)!")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    while True:
        print("\n--- Insecure User Data Manager ---")
        print("1. Search user (Command Injection flaw)")
        print("2. Save data (Insecure Deserialization & Directory Traversal flaws)")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username to search: ")
            search_user(username)
        elif choice == '2':
            filename = input("Enter filename to save data (e.g., 'data.pkl'): ")
            user_data = input("Enter data to save (e.g., 'some text'): ")
            save_data(filename, user_data)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
