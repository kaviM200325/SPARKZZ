import sqlite3
import hashlib
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the echoverse directory
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_DIR, 'users.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            age INTEGER,
            gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password, full_name, age, gender):
    password_hash = hash_password(password)
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, email, password_hash, full_name, age, gender) VALUES (?, ?, ?, ?, ?, ?)',
                     (username, email, password_hash, full_name, age, gender))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username or email already exists
    finally:
        conn.close()

def login_user(username_or_email, password):
    password_hash = hash_password(password)
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE (username = ? OR email = ?) AND password_hash = ?',
                        (username_or_email, username_or_email, password_hash)).fetchone()
    conn.close()
    return user

# Initialize database on import
create_tables()
