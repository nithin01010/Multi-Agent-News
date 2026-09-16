from langchain_core.tools import tool
import smtplib
from email.message import EmailMessage

from config import APP_PASSWORD, SENDER_EMAIL, SMTP_PORT, SMTP_SERVER


@tool
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
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("Email sent")
        return True
    except Exception as e:
        print("Error while sending mail, with:", e)
        return False


# if __name__ == "__main__":
#     e = Email()
#     e.send_email(
#         subject="testing",
#         body="working",
#         recipients=["nithinmyneni010@gmail.com"],
#         html_body="<h2>Testing HTML Email</h2><p>The email module now supports <strong>rich HTML</strong>!</p>",
#     )
