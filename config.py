from dotenv import load_dotenv
import os, mysql.connector

load_dotenv()

# Basic Database credentials that will be used to connect to the MySQL database and can easily be adjusted to suit your own database
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

# Other constants can be added here if you were to choose to grow the project and clean it up
DEFAULT_PASSWORD = "admin123"

def get_db_connection():
    """Return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)
