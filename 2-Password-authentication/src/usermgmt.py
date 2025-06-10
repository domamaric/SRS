import json
from getpass import getpass
from sys import argv, exit

from user import User


def add_user(username):
    password = getpass("Enter Password: ")
    repeat_password = getpass("Repeat Password: ")

    if password != repeat_password:
        exit("User add failed. Passwords do not match.")

    user = User(username)
    if user.add_password(password):
        print("User successfully added.")
    else:
        # Error message is handled within User.add_password
        pass


def change_password(username):
    new_password = getpass("Enter New Password: ")
    repeat_new_password = getpass("Repeat New Password: ")

    if new_password != repeat_new_password:
        exit("Password change failed. Passwords do not match.")

    user = User(username)
    if user.change_password(new_password):
        print("Password change successful.")
    else:
        # Error message is handled within User.change_password
        pass


def force_password_change(username):
    user = User(username)
    if user.set_force_password_change(True):
        print(f"User '{username}' will be requested to change password on next login.")
    else:
        # Error message is handled within User.set_force_password_change
        pass


def delete_user(username):
    user = User(username)
    if user.delete_user():
        print(f"User '{username}' successfully removed.")
    else:
        # Error message is handled within User.delete_user
        pass


if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: python usermgmt.py <command> <username>")
        print("Commands: add, passwd, forcepass, del")
        exit(1)

    command = argv[1].lower()
    username = argv[2]

    if command == "add":
        add_user(username)
    elif command == "passwd":
        change_password(username)
    elif command == "forcepass":
        force_password_change(username)
    elif command == "del":
        delete_user(username)
    else:
        print("Invalid command argument.")
        print("Commands: add, passwd, forcepass, del")
