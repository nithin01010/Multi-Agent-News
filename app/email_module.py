import smtplib
from email.message import EmailMessage

from config import APP_PASSWORD, SENDER_EMAIL, SMTP_PORT, SMTP_SERVER


def send_email(
    subject: str,
    recipients: list[str],
    html_body: str,
) -> bool:
    """This Function is used to send mail to recipients

    Args:
        subject (str): Subject of the email
        recipients (list[str]): Emails of all the users we need send mail
        html_body (str): the body content in terms of html code to good visual

    Returns:
        bool: True if mails are sent , else False
    """
    if isinstance(recipients, str):
        recipients = [recipients]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = SENDER_EMAIL
    msg["Bcc"] = ", ".join(recipients)

    msg.set_content(html_body, subtype="html")

    try:
        print(f"  Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f"  Email sent successfully to {len(recipients)} recipient(s)")
        return True
    except Exception as e:
        print(f"  Error sending email: {e}")
        return False
