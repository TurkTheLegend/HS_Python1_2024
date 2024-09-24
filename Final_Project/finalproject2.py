import os
import json
import bcrypt

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

def store_app_password(data, username, app_name, account_name, password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    if app_name not in data[username]["apps"]: 
        data[username]["apps"][app_name] = {}

    data[username]["apps"][app_name][account_name] = (hashed_password.decode('utf-8'), salt.decode('utf-8'))
    save_data(data)
    print(f"Password for {account_name} on {app_name} stored successfully!")

def retrieve_password(data, username, app_name, account_name, master_password):
    if username in data and app_name in data[username]["apps"] and account_name in data[username]["apps"][app_name]:
        hashed_password, salt = data[username]["apps"][app_name][account_name]
        if decrypt_password(hashed_password, salt, master_password):
            return master_password 
        else:
            print("Incorrect master password.")
    else:
        print("Credentials not found.")
    return None

def decrypt_password(hashed_password, salt, entered_password):
    entered_password_hashed = bcrypt.hashpw(entered_password.encode('utf-8'), salt.encode('utf-8'))
    return hashed_password == entered_password_hashed.decode('utf-8')

def main():
    while True:
        print("\nChoose an action:")
        print("1. Create Master Account")
        print("2. Login to Master Account")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username for your master account: ")
            while True:
                password = input("Enter master password: ")
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

            if username in data and decrypt_password(data[username]["master_password"][0], data[username]["master_password"][1], master_password):
                print("Login successful!")

                while True:
                    print("\nChoose an action:")
                    print("1. Register new app account")
                    print("2. Retrieve app account password")
                    print("3. Exit")

                    choice = input("Enter your choice: ")

                    if choice == '1':
                        app_name = input("Enter application name: ")
                        account_name = input("Enter account name: ")
                        password = input("Enter password: ")
                        store_app_password(data, username, app_name, account_name, password)

                    elif choice == '2':
                        if not user_data or len(user_data["apps"]) == 0:  # Check if there are any apps stored 
                            print("No stored passwords found.")
                            continue

                        print("\nYour applications:")
                        for i, app in enumerate(user_data["apps"].keys()): # Iterate over the 'apps' dictionary
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

                        password = retrieve_password(data, username, chosen_app, chosen_account, master_password)
                        if password:
                            print(f"Password for {chosen_account} on {chosen_app}: {password}")

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