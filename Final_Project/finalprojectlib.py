import os
import json
import hashlib

def store_password(username: str, password: str) -> None:
    print(hash_password(password))

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

store_password("Akarapong", "Akarapong")