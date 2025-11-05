import os

def run_command(command):
    os.system(command) # Insecure: Direct command execution with user input

# Vulnerable usage example
user_input = input("Enter a command: ")
# An attacker could input something like: "echo hello; rm -rf /"
run_command(f"echo {user_input}") 
