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
def save_password_func(category, name, username, password):
    user_id = get_user_id(username)  # Obtener el ID del usuario actual
    if user_id is None:
        print("Usuario no encontrado.")
        return

    save_password(user_id, category, name, username, password)  # Guardamos la contraseña


def open_password_manager():
    # Aquí se gestionan las contraseñas: ver, guardar, cambiar
    pass
