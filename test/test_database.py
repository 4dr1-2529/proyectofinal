from unittest.mock import MagicMock, patch
import unittest
from src.database import register_user, save_password, delete_user, create_tables, validate_login


class TestDatabase(unittest.TestCase):

    @patch('src.database.sqlite3.connect')
    def test_create_tables(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Llamamos a la función para crear las tablas
        create_tables()

        # Verificamos que las consultas para crear las tablas fueron ejecutadas
        mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS users (")

    @patch('src.database.sqlite3.connect')
    def test_delete_user(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_connect.return_value.commit = MagicMock()

        # Simulamos eliminar un usuario
        delete_user("testuser")

        # Verificamos que la consulta DELETE fue ejecutada correctamente
        mock_cursor.execute.assert_any_call(
            "DELETE FROM users WHERE username = ?",
            ("testuser",)
        )

    @patch('src.database.sqlite3.connect')
    def test_register_user(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_connect.return_value.commit = MagicMock()

        # Simular registro de usuario
        result = register_user("testuser", "password123", "test@example.com")
        self.assertTrue(result)

        # Verificamos que la consulta de inserción fue ejecutada correctamente
        mock_cursor.execute.assert_any_call(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            ("testuser", "password123", "test@example.com")
        )

    @patch('src.database.sqlite3.connect')
    def test_save_password(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_connect.return_value.commit = MagicMock()

        # Simulamos guardar una contraseña
        save_password(1, "category", "test_name", "test_username", "password123")

        # Verificamos que la consulta de inserción fue ejecutada correctamente
        mock_cursor.execute.assert_any_call(
            "INSERT INTO passwords (user_id, category, name, username, password) VALUES (?, ?, ?, ?, ?)",
            (1, "category", "test_name", "test_username", "password123")
        )

    @patch('src.database.sqlite3.connect')
    def test_validate_login(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)  # Simula que se encontró un usuario

        # Llamar a la función para validar login
        user_id = validate_login("testuser", "password123")

        # Verificamos que el ID de usuario es el correcto
        self.assertEqual(user_id, 1)  # La comparación debe ser correcta


if __name__ == '__main__':
    unittest.main()
