import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_password_reset_email(to_email, password):
    from_email = "your_email@example.com"
    from_password = "your_email_password"

    subject = "Password Reset Request"
    body = f"Your new password is: {password}"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Password reset email sent successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")
