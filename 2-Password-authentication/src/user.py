import json
from base64 import b64encode, b64decode
from os import urandom

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

class User:
    def __init__(self, username):
        self.username = username
        self.salt = None  # Will be loaded/generated per user
        self.password_hash = None # Will be loaded/generated per user

    def _derive_fernet_key(self, salt, password_raw):
        """Derives a Fernet key from the raw password and a unique salt."""
        # Using Scrypt for password hashing and key derivation
        kdf = Scrypt(
            salt=salt,
            length=32, # Fernet key length
            n=2**18,   # CPU/Memory cost parameter
            r=8,       # Block size parameter
            p=1,       # Parallelization parameter
            backend=default_backend()
        )
        derived_key = kdf.derive(password_raw.encode('utf-8'))
        return b64encode(derived_key) # Fernet key needs to be base64 encoded

    def _get_user_data(self, all_users_data):
        """Helper to find user data in the loaded JSON."""
        for user_data in all_users_data:
            if user_data["username"] == self.username:
                return user_data
        return None

    @staticmethod
    def _save_all_users_data(all_users_data):
        """Saves the entire list of user data to the database file."""
        with open("database.json", "w") as f:
            json.dump(all_users_data, f, indent=4, separators=(',', ': '))

    def add_password(self, password_raw):
        """
        Adds a new user with a password.
        Returns True on success, False if user already exists.
        """
        all_users_data = []
        try:
            with open("database.json", "r") as f:
                all_users_data = json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, create it and proceed
            with open("database.json", "w") as f:
                json.dump([], f)

        if self._get_user_data(all_users_data):
            # User already exists, cannot add
            print("Error: User already exists.")
            return False

        # Generate a unique salt for this user's password hash
        salt = urandom(16)

        # Derive Fernet key using Scrypt for strong password hashing
        fernet_key = self._derive_fernet_key(salt, password_raw)
        f = Fernet(fernet_key)

        # Encrypt a dummy value (or an empty string) using the derived key.
        # The fact that we can encrypt/decrypt this successfully means the key is correct.
        # This replaces the direct password encryption.
        # We're effectively storing a 'proof of key' rather than the password itself.
        # A simple 'confirmation' string is enough for verification.
        encrypted_proof = f.encrypt(b"key_verification_string")

        new_user_data = {
            "username": self.username,
            "force_password_change": False,
            "salt": b64encode(salt).decode('utf-8'), # Store salt in base64
            "key_proof": b64encode(encrypted_proof).decode('utf-8') # Store encrypted proof
        }

        all_users_data.append(new_user_data)
        self._save_all_users_data(all_users_data)
        return True

    def change_password(self, new_password_raw):
        """
        Changes the password for an existing user.
        Returns True on success, False if user does not exist.
        """
        all_users_data = []
        try:
            with open("database.json", "r") as f:
                all_users_data = json.load(f)
        except FileNotFoundError:
            print("Error: Database file not found.")
            return False

        user_found = False
        updated_users_data = []
        for user_data in all_users_data:
            if user_data["username"] == self.username:
                user_found = True
                # Generate a new salt for the new password
                new_salt = urandom(16)
                new_fernet_key = self._derive_fernet_key(new_salt, new_password_raw)
                new_f = Fernet(new_fernet_key)
                new_encrypted_proof = new_f.encrypt(b"key_verification_string")

                user_data["salt"] = b64encode(new_salt).decode('utf-8')
                user_data["key_proof"] = b64encode(new_encrypted_proof).decode('utf-8')
                user_data["force_password_change"] = False # Reset this flag after change
            updated_users_data.append(user_data)

        if not user_found:
            print("Error: User not found for password change.")
            return False

        self._save_all_users_data(updated_users_data)
        return True

    def verify_password(self, password_raw):
        """
        Verifies the provided password against the stored proof.
        Returns True if password is correct, False otherwise.
        """
        all_users_data = []
        try:
            with open("database.json", "r") as f:
                all_users_data = json.load(f)
        except FileNotFoundError:
            return False

        user_data = self._get_user_data(all_users_data)
        if not user_data:
            return False # User does not exist

        stored_salt = b64decode(user_data["salt"])
        stored_key_proof = b64decode(user_data["key_proof"])

        try:
            # Derive the key using the provided password and stored salt
            derived_fernet_key = self._derive_fernet_key(stored_salt, password_raw)
            f = Fernet(derived_fernet_key)
            
            # Attempt to decrypt the stored proof.
            # If the password is correct, decryption will succeed.
            # If incorrect, it will raise an InvalidToken exception.
            f.decrypt(stored_key_proof, ttl=None) # ttl=None means no expiry
            return True
        except Exception as e:
            # Any error during decryption means the password is incorrect or data is corrupt
            return False

    def set_force_password_change(self, force_change_status):
        """
        Sets or unsets the force password change flag for the user.
        """
        all_users_data = []
        try:
            with open("database.json", "r") as f:
                all_users_data = json.load(f)
        except FileNotFoundError:
            print("Error: Database file not found.")
            return False

        user_found = False
        updated_users_data = []
        for user_data in all_users_data:
            if user_data["username"] == self.username:
                user_found = True
                user_data["force_password_change"] = force_change_status
            updated_users_data.append(user_data)

        if not user_found:
            print("Error: User not found for force password change.")
            return False

        self._save_all_users_data(updated_users_data)
        return True

    def delete_user(self):
        """
        Deletes the user from the database.
        Returns True on success, False if user not found.
        """
        all_users_data = []
        try:
            with open("database.json", "r") as f:
                all_users_data = json.load(f)
        except FileNotFoundError:
            print("Error: Database file not found.")
            return False

        initial_len = len(all_users_data)
        updated_users_data = [
            user_data for user_data in all_users_data
            if not (user_data["username"] == self.username)
        ]

        if len(updated_users_data) == initial_len:
            print("Error: User not found for deletion.")
            return False

        self._save_all_users_data(updated_users_data)
        return True

    def needs_password_change(self):
        """Checks if the user is flagged for a forced password change."""
        try:
            with open("database.json", "r") as f:
                all_users_data = json.load(f)
        except FileNotFoundError:
            return False # Database doesn't exist, cannot check

        user_data = self._get_user_data(all_users_data)

        if user_data:
            return user_data.get("force_password_change", False)
        return False # User not found
