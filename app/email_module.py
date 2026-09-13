import smtplib
from email.message import EmailMessage

from config import APP_PASSWORD, SENDER_EMAIL, SMTP_PORT, SMTP_SERVER


class Email:
    def send_email(
        self,
        subject: str,
        body: str,
        recipients: list[str] | str,
        html_body: str | None = None,
    ) -> bool:
        if isinstance(recipients, str):
            recipients = [recipients]

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = SENDER_EMAIL
        msg["Bcc"] = ", ".join(recipients)
        msg.set_content(body)
        
        # HTML content if provided
        if html_body:
            msg.add_alternative(html_body, subtype="html")

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)
            print("Email sent")
            return True
        except Exception as e:
            print("Error while sending mail, with:", e)
            return False


if __name__ == "__main__":
    e = Email()
    e.send_email(
        subject="testing",
        body="working",
        recipients=["nithinmyneni010@gmail.com"],
        html_body="<h2>Testing HTML Email</h2><p>The email module now supports <strong>rich HTML</strong>!</p>",
    )