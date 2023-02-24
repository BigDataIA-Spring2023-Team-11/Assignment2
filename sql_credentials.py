# from passlib.context import CryptContext
import os
import sqlite3
import bcrypt
from pathlib import Path
import pandas as pd
import logging


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


database_file_name = "meta.db"
database_file_path  = os.path.join(os.path.dirname(__file__),database_file_name)

table_name = "cred"

# def get_hashed_password(password):
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

def verify_password(db_password,given_password):
    flag = 0
    if str(hash_text(given_password)) == str(db_password):
        flag = 1
    return flag



import hashlib

def hash_text(text):
    # Convert the text to bytes using UTF-8 encoding
    text_bytes = text.encode('utf-8')

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the text bytes
    sha256_hash.update(text_bytes)

    # Get the hexadecimal representation of the hash
    hex_digest = sha256_hash.hexdigest()

    # Return the hexadecimal hash digest
    return hex_digest

def add_user_to_table(username, password):
    # Connect to the database
    conn = sqlite3.connect('../meta.db')
    c = conn.cursor()
    tableName = "cred"
    # Insert the new user into the table
    c.execute(f"Create TABLE IF NOT EXISTS {tableName} (username,password);")
    c.execute("INSERT INTO cred (username, password) VALUES (?, ?)", (username, password))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# if __name__ == "__main__":
#     # pwd = hash_text("spring2023")
#     # add_user_to_table('damg7245', pwd)
