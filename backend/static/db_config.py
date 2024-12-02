import os
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file only if not running on App Engine
if os.environ.get('GAE_ENV') != 'standard':
    from dotenv import load_dotenv
    load_dotenv()

# Database configuration using environment variables
db_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME'],
    'port': int(os.environ.get('DB_PORT', 3306))
}

# Function to establish a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Successful connection to DB")
            return conn
    except Error as txt:
        print(f"Error connecting to MySQL: {txt}")
    return None
