import smtplib
from email.message import EmailMessage

from config import APP_PASSWORD, SENDER_EMAIL, SMTP_PORT, SMTP_SERVER


class Email:
    def send_email(self, subject: str, body: str, recipients: list[str]):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = SENDER_EMAIL
        msg["Bcc"] = ", ".join(recipients)
        msg.set_content(body)
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
            print("Email sent")
            return True
        except Exception as e:
            print("Error while sending mail, with:", e)
            return False