import os
import json
import bcrypt

def store_password(username: str, password: str) -> None:
    if not username or not password:
        print("Error: Username and password cannot be empty.")
        return None
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
    print(f"Password for username '{username}' stored successfully!")


def retrive_password(username: str) -> tuple:
    if not username:
        print("Error: Username cannot be empty")
        return None, None
    if not os.path.exists('data.json'):
        print("Error: No stored passwords found.")
        return None, None
    with open('data.json', 'r') as f:
        data = json.load(f)
    if usename in data:
        return data[username][0], data[username][1] # Hashed
    else:
        print(f"Error: Username '{username}' not found.")
        return None, None

def clear_screen() -> None:
    os.system('clear')

def decrypt_password(hashed_password: bytes) -> str:
    pass


print(salt)