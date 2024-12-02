import unittest
from unittest.mock import patch, MagicMock
from src.database import create_tables, register_user, save_password, validate_login


class TestDatabase(unittest.TestCase):

    @patch('src.database.sqlite3.connect')
    def test_create_tables(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Llamamos a la función para crear las tablas
        create_tables()

        # Normalizamos la consulta para compararla de manera más flexible
        expected_sql_users = '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )
        '''.strip().replace('\n', '').replace(' ', '')

        expected_sql_passwords = '''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''.strip().replace('\n', '').replace(' ', '')

        # Verificamos que las consultas CREATE TABLE fueron ejecutadas correctamente
        actual_calls = [call[0][0].replace('\n', '').replace(' ', '') for call in mock_cursor.execute.call_args_list]

        self.assertTrue(expected_sql_users in actual_calls)
        self.assertTrue(expected_sql_passwords in actual_calls)

    @patch('src.database.sqlite3.connect')
    def test_register_user(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Llamamos a la función para registrar un usuario
        register_user('testuser', 'password123', 'testuser@example.com')

        # Verificamos que la consulta de inserción fue ejecutada
        mock_cursor.execute.assert_called_with(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            ('testuser', 'password123', 'testuser@example.com')
        )

    @patch('src.database.sqlite3.connect')
    def test_save_password(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Llamamos a la función para guardar una contraseña
        save_password(1, 'Social Media', 'Facebook', 'fbuser', 'fbpassword123')

        # Verificamos que la consulta de inserción fue ejecutada
        mock_cursor.execute.assert_called_with(
            "INSERT INTO passwords (user_id, category, name, username, password) VALUES (?, ?, ?, ?, ?)",
            (1, 'Social Media', 'Facebook', 'fbuser', 'fbpassword123')
        )

    @patch('src.database.sqlite3.connect')
    def test_validate_login(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'testuser', 'password123', 'testuser@example.com')

        # Llamamos a la función para validar el inicio de sesión
        result = validate_login('testuser', 'password123')

        # Verificamos que la función retorne True para un inicio de sesión válido
        self.assertTrue(result)
        mock_cursor.execute.assert_called_with(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            ('testuser', 'password123')
        )


if __name__ == '__main__':
    unittest.main()
