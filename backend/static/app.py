from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template, session, flash
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
import sys

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)    #Allow frontend to communicate with the backend

# Path to groceryapp.sql
sql_file_path = os.path.join("..", "database", "groceryapp.sql")

# Demo Groceries to test functionalit
groceries = [
    {"id": 1, "name": "Milk", "quantity": 1},
    {"id": 1, "name": "Eggs", "quantity": 12}
]

# MySQL database configuration
# Will need to go though and change values to match our values
db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'database': 'GroceryApp'
}

# Reads and executes SQL commands from groceryapp.sql
def execute_sql_file(connection, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()  # Read the entire file as a single string
    cursor = connection.cursor()
    try:
        cursor.execute(sql_script, multi=True)  # Execute multiple statements at once
        connection.commit()
    except Error as e:
        print(f"Error executing SQL script: {e}")
    finally:
        cursor.close()

# To establish MySQL connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Function to initialize the database
# Keeping this here to reference just incase execute_sql_file() doesn't work
"""def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Specify the path to the groceryapp.sql file
    sql_file_path = '../database/groceryapp.sql'  # Adjust this path as needed
    with open(sql_file_path, "r") as sql_file:
        sql_commands = sql_file.read().split(';')
        for command in sql_commands:
            if command.strip():  # Ignore empty commands
                cursor.execute(command)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")"""

@app.route('/api/<username>/groceries', methods=['GET'])
def get_groceries(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT i.inventory_id AS id, f.food_name AS name, i.quantity 
        FROM GroceryApp.Inventory i 
        JOIN GroceryApp.Users u ON i.user_id = u.user_id 
        JOIN GroceryApp.AllFoods f ON i.food_id = f.food_id 
        WHERE u.user_name = %s
    """
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results), 200

# @app.route('/api/<username>/groceries', methods={'POST'}) # Added /<username> so we know who's groceries we're adding to
@app.route('/api/groceries', methods={'POST'})
def add_grocery(username):
    new_item = request.json()
    groceries.append(new_item)
    return jsonify(new_item), 201

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    # Serve Vue frontend files
    if path != "" and os.path.exists(f"static/{path}"):
        return send_from_directory('static', path)
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    # Initialize the database connection
    conn = get_db_connection()

    # Specify the path to the groceryapp.sql file
    sql_file_path = '../database/groceryapp.sql'  # Adjust this path as needed

    # Call the function to execute the SQL file
    execute_sql_file(conn, sql_file_path)

    # Close the connection
    conn.close()

    app.run(debug=True)
