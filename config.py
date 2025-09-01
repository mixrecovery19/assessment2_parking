from dotenv import load_dotenv
import os, mysql.connector

load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "carpark")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Optional: central db_config dictionary
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}

# Other constants
DEFAULT_PASSWORD = "admin123"

def get_db_connection():
    """Return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)
