import argparse
import json
import os
from base64 import b64encode, b64decode
from pathlib import Path

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets


class PasswordManager:
    DB_FILE = Path('./passwords.json')
    SALT_FILE = Path('./salt.bin')
    
    def __init__(self, master_password):
        self._master_password = master_password.encode('utf-8')
        
    def initialize(self):
        """Initialize an empty password database with a new salt."""
        # Generate a random salt, one more secure than 'tinf srs uui'
        salt = secrets.token_bytes(16)
        
        # Save the salt
        with open(self.SALT_FILE, 'wb') as f:
            f.write(salt)
            
        # Create an empty database
        with open(self.DB_FILE, 'w') as f:
            json.dump([], f)
            
        return True
        
    def derive_key(self):
        """Derive encryption key from master password using the stored salt."""
        try:
            with open(self.SALT_FILE, 'rb') as f:
                salt = f.read()

            # Arbitrary parameter selection, however my hardware is slow :(
            kdf = Scrypt(
                salt=salt,
                length=32,
                n=2**18,   # CPU/memory cost parameter
                r=8,       # Block size parameter
                p=1        # Parallelization parameter
            )
            
            key = kdf.derive(self._master_password)
            return key
        except FileNotFoundError:
            raise Exception("Password manager not initialized. Run with --init first.")
    
    def verify_master_password(self):
        """Verify if the provided master password is correct."""
        try:
            key = self.derive_key()
            
            # If no entries exist, check if the database file exists
            if not os.path.exists(self.DB_FILE):
                raise Exception("Password manager not initialized or database corrupted.")
                
            return True
        except Exception as e:
            return False
            
    def save_password(self, address, password):
        """Store or update a password for a given address."""
        if not self.verify_master_password():
            return False, "Master password incorrect or database corrupted."
            
        key = self.derive_key()
        
        try:
            # Load existing database
            with open(self.DB_FILE, 'r') as f:
                try:
                    entries = json.load(f)
                except json.JSONDecodeError:
                    entries = []

            aesgcm = AESGCM(key)
            nonce = secrets.token_bytes(12)  # 96-bit nonce for AES-GCM
            
            # Combine address and password for encryption
            data = f"{address},{password}".encode('utf-8')
            ciphertext = aesgcm.encrypt(nonce, data, None)
            
            # Create entry with base64 encoded values for JSON storage
            new_entry = {
                "nonce": b64encode(nonce).decode('utf-8'),
                "ciphertext": b64encode(ciphertext).decode('utf-8')
            }
            
            # Remove existing entry for this address if it exists
            entries = [e for e in entries if self._decrypt_entry(e, key).split(',')[0] != address]

            entries.append(new_entry)
            
            # Save the updated database
            with open(self.DB_FILE, 'w') as f:
                json.dump(entries, f)
                
            return True, f"Stored password for {address}."
            
        except Exception as e:
            return False, f"Error saving password: {str(e)}"
    
    def _decrypt_entry(self, entry, key):
        """Helper to decrypt a single entry using the provided key."""
        nonce = b64decode(entry["nonce"])
        ciphertext = b64decode(entry["ciphertext"])
        
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        
        return plaintext.decode('utf-8')
    
    def get_password(self, address):
        """Retrieve a password for a given address."""
        if not self.verify_master_password():
            return False, "Master password incorrect or database corrupted."
            
        key = self.derive_key()
        
        try:
            with open(self.DB_FILE, 'r') as f:
                try:
                    entries = json.load(f)
                except json.JSONDecodeError:
                    return False, "Database is empty or corrupted."
            
            # Search for the address
            for entry in entries:
                try:
                    data = self._decrypt_entry(entry, key)
                    stored_address, stored_password = data.split(',', 1)
                    
                    if stored_address == address:
                        return True, stored_password
                except Exception:
                    # Skip entries that fail to decrypt
                    continue
            
            return False, f"No password found for {address}."
            
        except Exception as e:
            return False, f"Error retrieving password: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description='Secure Password Manager')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init', type=str, metavar='MASTER_PASSWORD',
                       help='Initialize password manager with master password')
    group.add_argument('--put', nargs=3, metavar=('MASTER_PASSWORD', 'ADDRESS', 'PASSWORD'),
                       help='Store password for an address')
    group.add_argument('--get', nargs=2, metavar=('MASTER_PASSWORD', 'ADDRESS'),
                       help='Retrieve password for an address')
    
    args = parser.parse_args()
    
    if args.init:
        pm = PasswordManager(args.init)
        pm.initialize()
        print("Password manager initialized.")
    elif args.put:
        master_password, address, password = args.put
        pm = PasswordManager(master_password)
        success, message = pm.save_password(address, password)
        print(message)
    elif args.get:
        master_password, address = args.get
        pm = PasswordManager(master_password)
        success, result = pm.get_password(address)
        
        if success:
            print(f"Password for {address} is: {result}")
        else:
            print(result)

if __name__ == '__main__':
    main()
