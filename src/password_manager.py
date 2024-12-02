import random
import string
from database import save_password, get_user_id

# Generar contraseña segura
def generate_secure_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(random.choice(characters) for i in range(12))
    return secure_password

# Mostrar contraseñas guardadas
def show_passwords():
    # Función para obtener y mostrar contraseñas de la base de datos
    pass

# Guardar contraseña en la base de datos
def save_password(category, name, username, password):
    user_id = get_user_id()  # Obtener el ID del usuario actual
    conn = sqlite3.connect('passkeeper.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (user_id, category, name, username, password)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, category, name, username, password))
    conn.commit()
    conn.close()

def open_password_manager():
    # Aquí se gestionan las contraseñas: ver, guardar, cambiar
    pass
