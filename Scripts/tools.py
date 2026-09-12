import os
import smtplib

from dotenv import load_dotenv
from langchain.tools import tool
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()


@tool
def send_mail(subject: str, body: str) -> str:
    """
    Send an email to the configured receiver.

    Args:
        subject: Subject of the email.
        body: Body/content of the email.

    Returns:
        A message indicating whether the email was sent successfully.
    """

    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    email_password = os.getenv("EMAIL_PASSWORD")

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Validate environment variables
    if not sender_email:
        return "Email failed: EMAIL_SENDER is not configured."

    if not receiver_email:
        return "Email failed: EMAIL_RECEIVER is not configured."

    if not email_password:
        return "Email failed: EMAIL_PASSWORD is not configured."

    # Create email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Attach email body
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, email_password)

            server.sendmail(
                sender_email,
                receiver_email,
                msg.as_string()
            )

        return "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        return "Email failed: SMTP authentication failed. Check your Gmail credentials/app password."

    except Exception as e:
        return f"Email failed: {str(e)}"




# For testing purpose only

# result = send_mail.invoke({
#     "subject": "Test Email — News Recommendation Agent",
#     "body": """Hello!

# This is a test email from my News Recommendation Agent.

# If you received this email, the send_mail tool is working correctly.

# Test reference:
# Song: Señorita — Shawn Mendes & Camila Cabello
# Excerpt: "I wish it wasn't so hard to leave ya"

# Next step: connect this tool to the news-generation agent.

# Regards,
# News Recommendation Agent
# """
# })

# print(result)