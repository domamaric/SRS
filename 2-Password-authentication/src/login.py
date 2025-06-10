import json
from getpass import getpass
from sys import argv, exit

from user import User 

def main(username):
    user = User(username)
    entered_password = getpass("Enter Password: ")

    if not user.verify_password(entered_password):
        print("Username or password incorrect.")
        return # Exit if login fails

    print("Login successful.")

    # Check if a forced password change is required
    if user.needs_password_change():
        print("You are required to change your password.")
        new_password = getpass("Enter New Password: ")
        repeat_new_password = getpass("Repeat New Password: ")

        if new_password != repeat_new_password:
            print("Password change failed. Passwords do not match.")
            # In a real system, you might want to log out here or disable the account.
            # For this exercise, we'll just indicate failure and exit gracefully.
            return

        if user.change_password(new_password):
            print("Password successfully changed.")
        else:
            print("Password change failed during update. Please contact administrator.")
            # This indicates an issue writing to the database, might be permissions etc.


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python login.py <username>")
        exit(1)

    username = argv[1]
    main(username)