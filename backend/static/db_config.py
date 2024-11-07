import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# Database configuration using environment variables
# Enter in your credentials withing the .env file
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
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

