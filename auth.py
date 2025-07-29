import bcrypt
import json
import os

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed
    save_users(users)
    return True

def login_user(username, password):
    users = load_users()
    if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
        return True
    return False

def reset_password(username, new_password):
    users = load_users()
    if username in users:
        users[username] = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        save_users(users)
        return True
    return False