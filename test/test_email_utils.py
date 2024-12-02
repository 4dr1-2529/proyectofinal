import unittest
from unittest.mock import patch, MagicMock
from src.email_utils import send_password_reset_email
import re

class TestEmailUtils(unittest.TestCase):

    @patch('src.email_utils.smtplib.SMTP')
    def test_send_password_reset_email(self, MockSMTP):
        # Crear un objeto mock para la instancia de SMTP
        mock_smtp_instance = MagicMock()
        MockSMTP.return_value = mock_smtp_instance

        # Simular el envío del correo
        send_password_reset_email("test@example.com", "newpassword123")

        # Verificar que el correo fue enviado
        args, _ = mock_smtp_instance.sendmail.call_args
        message = args[2]  # El cuerpo del mensaje es el tercer argumento en la llamada a sendmail

        # Comprobar que el mensaje contiene la dirección del remitente y destinatario
        self.assertIn("your_email@example.com", message)
        self.assertIn("test@example.com", message)

        # Verificar que el asunto y el cuerpo contengan lo esperado
        self.assertIn("Subject: Password Reset Request", message)
        self.assertIn("Your new password is: newpassword123", message)

        # Verificar que la longitud del boundary es razonable (por ejemplo, más de 10 caracteres)
        boundary_match = re.search(r'boundary="(.*?)"', message)
        self.assertIsNotNone(boundary_match)
        self.assertGreater(len(boundary_match.group(1)), 10)

if __name__ == '__main__':
    unittest.main()
