import json
import os

DB_FILE = "user_data.json"

def load_user_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def register(username, password):
    data = load_user_data()
    if username in data:
        return False
    data[username] = {
        "password": password,
        "phq9": None,
        "gad7": None,
        "journal": [],
        "mood": [],
        "chat": []
    }
    save_user_data(data)
    return True

def login(username, password):
    data = load_user_data()
    return username in data and data[username]["password"] == password
