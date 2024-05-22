from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

SECRET_AUTH = os.environ.get("SECRET_AUTH")