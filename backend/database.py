import json
import os
from datetime import datetime
from uuid import uuid4

DATA_DIR = "../data-examples"
os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"prompts": [], "templates": [], "tokens": {"total": 100000, "used": 0}}

def save_json(data, filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def deduct_tokens(amount: int = 10):
    data = load_json("tokens.json")
    data["tokens"]["used"] += amount
    save_json(data, "tokens.json")
    return data["tokens"]["total"] - data["tokens"]["used"] >= 0