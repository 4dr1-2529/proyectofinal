import unittest
import sys
import os

# Añadir src al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Ahora importa los módulos desde src
from password_manager import save_password, generate_secure_password
from database import save_password as db_save_password, get_user_id


class TestPasswordManager(unittest.TestCase):

    def test_generate_secure_password(self):
        # Test para verificar que se genera una contraseña segura
        password = generate_secure_password()
        self.assertTrue(len(password) >= 12)  # Verificar que la longitud es al menos 12 caracteres
        self.assertTrue(any(c.isdigit() for c in password))  # Verificar que contiene un número
        self.assertTrue(any(c.isalpha() for c in password))  # Verificar que contiene una letra

    def test_save_password(self):
        # Supongamos que el id de usuario es 1
        user_id = 1
        category = "test_category"
        name = "test_name"
        username = "test_username"
        password = "test_password"

        # Guardar la contraseña usando la función
        db_save_password(user_id, category, name, username, password)

        # Aquí puedes verificar si la contraseña fue realmente guardada en la base de datos
        # Agregar la lógica para consultar la base de datos y verificar si la contraseña fue guardada


if __name__ == '__main__':
    unittest.main()
