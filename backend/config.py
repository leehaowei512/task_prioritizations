# config.py
import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Constants
JSON_FILE_PATH = "data.json"


def get_database_url():
    """Construct database URL from environment variables"""
    return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
