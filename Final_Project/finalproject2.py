import os
import json
import base64
import bcrypt
from cryptography.fernet import Fernet

def get_data():
    if not os.path.exists('data.json'):
        return {}
    with open('data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def store_master_password(data, username, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    data[username] = {"master_password": (hashed_password.decode('utf-8'), salt.decode('utf-8')), "apps": {}}
    save_data(data)
    print("Master password stored successfully!")

def store_app_password(data, username, app_name, account_name, password, master_password):
    salt = bcrypt.gensalt()
    key = bcrypt.kdf(
        password=master_password.encode('utf-8'),
        salt=salt,
        desired_key_bytes=32,
        rounds=100  # Increased rounds for security
    )
    b64_key = base64.urlsafe_b64encode(key)
    f = Fernet(b64_key)
    encrypted_password = f.encrypt(password.encode('utf-8')).decode('utf-8')

    if app_name not in data[username]["apps"]:
        data[username]["apps"][app_name] = {}

    data[username]["apps"][app_name][account_name] = (encrypted_password, salt.decode('utf-8'))
    save_data(data)
    print(f"Password for {account_name} on {app_name} stored successfully!")

def retrieve_app_password(data, username, app_name, account_name, master_password):
    if username in data and app_name in data[username]["apps"] and account_name in data[username]["apps"][app_name]:
        stored_master_password_hash, salt = data[username]["master_password"]
        if bcrypt.checkpw(master_password.encode('utf-8'), stored_master_password_hash.encode('utf-8')):
            encrypted_app_password, app_salt = data[username]["apps"][app_name][account_name]
            key = bcrypt.kdf(
                password=master_password.encode('utf-8'),
                salt=app_salt.encode('utf-8'),
                desired_key_bytes=32,
                rounds=100  # Must match store_app_password
            )
            b64_key = base64.urlsafe_b64encode(key)
            f = Fernet(b64_key)
            decrypted_app_password = f.decrypt(encrypted_app_password.encode('utf-8')).decode('utf-8')
            return decrypted_app_password
        else:
            print("Incorrect master password.")
    else:
        print("Credentials not found.")
    return None

def main():
    while True:
        print("\nChoose an action:")
        print("1. Create Master Account")
        print("2. Login to Master Account")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username for your master account: ").strip()
            while username == "":
                username = input("Enter username for your master account: ").strip()
            while True:
                password = input("Enter master password: ").strip()
                while password == "":
                    password = input("Enter master password: ").strip()
                confirm_password = input("Confirm master password: ")
                if password == confirm_password:
                    store_master_password(get_data(), username, password)
                    break
                else:
                    print("Passwords do not match. Please try again.")

        elif choice == '2':
            username = input("Enter username: ")
            master_password = input("Enter master password: ")

            data = get_data()
            user_data = data.get(username)

            if username in data and bcrypt.checkpw(master_password.encode('utf-8'), data[username]["master_password"][0].encode('utf-8')):
                print("Login successful!")

                while True:
                    print("\nChoose an action:")
                    print("1. Register new app account")
                    print("2. Retrieve app account password")
                    print("3. Exit")

                    choice = input("Enter your choice: ")

                    if choice == '1':
                        app_name = input("Enter application name: ")
                        account_name = input("Enter account username: ").strip()
                        while account_name == "":
                            account_name = input("Enter account username: ").strip()
                        password = input("Enter password: ").strip()
                        while password == "":
                            password = input(("Enter password: ")).strip()
                        store_app_password(data, username, app_name, account_name, password, master_password)

                    elif choice == '2':
                        if not user_data or not user_data.get("apps"):
                            print("No stored passwords found.")
                            continue

                        print("\nYour applications:")
                        for i, app in enumerate(user_data["apps"].keys()):
                            print(f"{i+1}. {app}")

                        try:
                            app_choice = int(input("Choose an application: ")) - 1
                            chosen_app = list(user_data["apps"].keys())[app_choice]
                        except (ValueError, IndexError):
                            print("Invalid application choice.")
                            continue

                        print("\nYour accounts for this application:")
                        for i, account in enumerate(user_data["apps"][chosen_app].keys()):
                            print(f"{i+1}. {account}")

                        try:
                            account_choice = int(input("Choose an account: ")) - 1
                            chosen_account = list(user_data["apps"][chosen_app].keys())[account_choice]
                        except (ValueError, IndexError):
                            print("Invalid account choice.")
                            continue

                        app_password = retrieve_app_password(data, username, chosen_app, chosen_account, master_password)
                        if app_password:
                            print(f"Password for {chosen_account} on {chosen_app}: {app_password}")

                    elif choice == '3':
                        break
                    else:
                        print("Invalid choice.")

            else:
                print("Incorrect master password or username not found.")

        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()