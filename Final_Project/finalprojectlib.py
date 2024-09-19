import os
import json
import hashlib

def store_password(username: str, password: str) -> None:
    hashed_password = hash_password(password)
    hashed_password_hex = hashed_password.hex()
    data = {username: hashed_password_hex}
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            existing_data = json.load(f)
        existing_data.update(data)
    else:
        existing_data = data

    with open('data.json', 'w') as f:
        json.dump(existing_data, f)

def hash_password(password: str) -> bytes:
    password = bytes(password, "utf-8")
    hashed_password = hashlib.sha384(password).digest()
    return hashed_password

def retrived_password() -> None:
    pass

def clear_screen() -> None:
    os.system('clear')

def authenticate() -> None:
    pass

store_password("็Harbour", "Space")