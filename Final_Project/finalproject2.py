import os
import json
import base64

import bcrypt
from cryptography.fernet import Fernet


def load_data() -> dict:
    """Loads user data from a JSON file."""
    if not os.path.exists("data.json"):
        return {}
    with open("data.json", "r") as f:
        return json.load(f)


def save_data(data: dict):
    """Saves user data to a JSON file."""
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


def store_master_password(data: dict, username: str, password: str) -> None:
    """Stores the master password securely."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    data[username] = {
        "master_password": (hashed_password.decode("utf-8"), 
                            salt.decode("utf-8")),
        "apps": {},
    }
    save_data(data)
    print("Master password stored successfully!")


def store_app_password(
    data: dict, username: str, app_name: str, account_name: str, 
    password: str, master_password: str
) -> None:
    """Encrypts and stores an app password using the master password."""
    salt = bcrypt.gensalt()
    key = bcrypt.kdf(
        password=master_password.encode("utf-8"),
        salt=salt,
        desired_key_bytes=32,
        rounds=100, 
    )
    b64_key = base64.urlsafe_b64encode(key)
    f = Fernet(b64_key)
    encrypted_password = f.encrypt(password.encode("utf-8")).decode("utf-8")

    if app_name not in data[username]["apps"]:
        data[username]["apps"][app_name] = {}

    data[username]["apps"][app_name][account_name] = (
        encrypted_password,
        salt.decode("utf-8"),
    )
    save_data(data)
    print(f"Password for {account_name} on {app_name} stored successfully!")


def retrieve_app_password(
    data: dict, username: str, app_name: str, account_name: str, 
    master_password: str
) -> str:
    """Retrieves and decrypts a stored app password."""
    if (
        username in data
        and app_name in data[username]["apps"]
        and account_name in data[username]["apps"][app_name]
    ):
        stored_master_password_hash, _ = data[username]["master_password"]
        if bcrypt.checkpw(
            master_password.encode("utf-8"),
            stored_master_password_hash.encode("utf-8"),
        ):
            encrypted_app_password, app_salt = \
                data[username]["apps"][app_name][account_name]
            key = bcrypt.kdf(
                password=master_password.encode("utf-8"),
                salt=app_salt.encode("utf-8"),
                desired_key_bytes=32,
                rounds=100, 
            )
            b64_key = base64.urlsafe_b64encode(key)
            f = Fernet(b64_key)
            decrypted_app_password = f.decrypt(
                encrypted_app_password.encode("utf-8")
            ).decode("utf-8")
            return decrypted_app_password
        else:
            print("Incorrect master password.")
    else:
        print("Credentials not found.")
    return None


def main():
    """Main function to handle user interaction and password management."""


if __name__ == "__main__":
    main()