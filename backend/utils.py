# utils.py
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
invalid_tokens = set()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')
