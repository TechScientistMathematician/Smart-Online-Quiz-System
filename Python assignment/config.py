import hashlib
import json
from pathlib import Path

CONFIG_FILE = Path('data/admin_config.json')


def get_config():
    if not CONFIG_FILE.exists():
        return {
            'admin_email': '',
            'password_hash': '',
            'security_questions': {
                'question1': 'What city were you born in?',
                'question2': 'What was the name of your first pet?'
            },
            'answers_hash': ''
        }

    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(config):
    CONFIG_FILE.parent.mkdir(exist_ok=True, parents=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def hash_value(value, salt='SOQS_SALT'):
    return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    return True, ""
