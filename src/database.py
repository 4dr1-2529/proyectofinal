import sqlite3


def connect_db():
    return sqlite3.connect('password_manager.db')


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()


def register_user(username, password, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
    conn.commit()
    conn.close()


def save_password(user_id, category, name, username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (user_id, category, name, username, password) VALUES (?, ?, ?, ?, ?)",
                   (user_id, category, name, username, password))
    conn.commit()
    conn.close()


def validate_login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_user_id(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]  # Retorna el id del usuario
    else:
        return None  # Si no se encuentra el usuario, retorna None
