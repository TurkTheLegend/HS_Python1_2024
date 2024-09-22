import os
import json
import bcrypt

def store_password(username: str, password: str) -> None:
    salt = bcrypt.gensalt()
    pass



def retrived_password(username: str) -> str:
    pass

def clear_screen() -> None:
    os.system('clear')

salt = bcrypt.gensalt()
print(salt)