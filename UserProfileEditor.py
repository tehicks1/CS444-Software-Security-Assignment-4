import os

def create_profile():
    username = input("Enter username: ")
    password = input("Enter password: ")
    bio = input("Enter your bio: ")

    with open(f"{username}.txt", "w") as f:
        f.write(f"Username: {username}\n")
        f.write(f"Password: {password}\n") # Security Flaw 1: Storing plaintext password
        f.write(f"Bio: {bio}\n")
    print("Profile created successfully!")

def view_profile():
    username = input("Enter username to view: ")
    try:
        with open(f"{username}.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("Profile not found.")

def update_bio():
    username = input("Enter username to update bio: ")
    new_bio = input("Enter new bio: ")
    
    # Security Flaw 2: Insecure file handling/path traversal
    # Allows updating any file if "username" contains path elements (e.g., ../../secret.txt)
    try:
        with open(f"{username}.txt", "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if line.startswith("Bio:"):
                    f.write(f"Bio: {new_bio}\n")
                else:
                    f.write(line)
            f.truncate()
        print("Bio updated successfully!")
    except FileNotFoundError:
        print("Profile not found.")

def delete_profile():
    username = input("Enter username to delete: ")
    # Security Flaw 3: Insecure file deletion (path traversal)
    # Allows deleting any file if "username" contains path elements
    try:
        os.remove(f"{username}.txt")
        print("Profile deleted successfully!")
    except FileNotFoundError:
        print("Profile not found.")

def execute_command():
    command = input("Enter command to execute (admin only): ")
    # Security Flaw 4: Command Injection
    # Allows executing arbitrary system commands
    os.system(command)

def main():
    while True:
        print("\n1. Create Profile")
        print("2. View Profile")
        print("3. Update Bio")
        print("4. Delete Profile")
        print("5. Execute Command (Admin)")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            create_profile()
        elif choice == '2':
            view_profile()
        elif choice == '3':
            update_bio()
        elif choice == '4':
            delete_profile()
        elif choice == '5':
            execute_command()
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
