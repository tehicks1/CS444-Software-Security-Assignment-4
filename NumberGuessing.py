import random
import os

def guess_the_number():
    secret_number = random.randint(1, 100)
    attempts = 0
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        try:
            user_guess_str = input("Enter your guess: ")
            # Flaw 1: Insecure use of eval()
            user_guess = eval(user_guess_str) 

            attempts += 1

            if user_guess < secret_number:
                print("Too low!")
            elif user_guess > secret_number:
                print("Too high!")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
        except Exception as e:
            # Flaw 2: Broad exception handling revealing internal errors
            print(f"An error occurred: {e}")

    # Flaw 3: Unsanitized user input in a shell command
    username = input("Enter your username for the leaderboard: ")
    os.system(f"echo {username} - {attempts} attempts >> leaderboard.txt") 

    # Flaw 4: Hardcoded sensitive information (simulated)
    admin_password = "supersecretpassword123" 
    if input("Enter admin password to view full leaderboard: ") == admin_password:
        with open("leaderboard.txt", "r") as f:
            print("\n--- Full Leaderboard ---")
            print(f.read())
    else:
        print("Incorrect password.")

    # Flaw 5: Lack of input validation for file operations (simulated)
    log_filename = input("Enter a filename to log your game details (e.g., my_game.log): ")
    with open(log_filename, "w") as f:
        f.write(f"Game played by: {username}, Guesses: {attempts}\n")
    print(f"Game details logged to {log_filename}")

if __name__ == "__main__":
    guess_the_number()

