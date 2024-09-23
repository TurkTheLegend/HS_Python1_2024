import os
import json
import bcrypt

def store_password(username: str, password: str) -> None:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    data = {username: (hashed_password.decode('utf-8'), salt.decode('utf-8'))}
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            existing_data = json.load(f)
        existing_data.update(data)
    else:
        existing_data = data
    with open('data.json', 'w') as f:
        json.dump(existing_data, f)


def retrived_password(username: str) -> str:
    pass

def clear_screen() -> None:
    os.system('clear')

def decrypt_password(hashed_password: bytes) -> str:
    pass

salt = bcrypt.gensalt()
print(salt)