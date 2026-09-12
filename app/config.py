import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the app
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
load_dotenv(dotenv_path=BASE_DIR / ".env")

# Email configurations
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("sender_email")
APP_PASSWORD = os.getenv("app_password")
