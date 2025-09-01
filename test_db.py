import os
from dotenv import load_dotenv
import mysql.connector

# Load variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Test connection
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("✅ Connection successful!")
except mysql.connector.Error as e:
    print(f"❌ Connection failed: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
