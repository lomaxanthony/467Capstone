# I (with a lot of help from Github Copilit) did a lot of adjusting to the backend file so that I could get adding a new user, 
# having the user login, and then adding a new grocery item to the database.


from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template, session, flash
from flask_session import Session
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
import mysql.connector
from mysql.connector import Error
import os
import sys
from db_config import get_db_connection
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import secrets
import logging


load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')

SECRET_KEY = 'G0kulTh3GO@T'
app.secret_key = os.getenv('SECRET_KEY')
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
    SESSION_TYPE='filesystem'
)
app.config.from_object(__name__)
bcrypt = Bcrypt(app)
Session(app)

###### TRYING A NEW APPROACH TO THE COOKIE MADNESS ######
# Set a secure secret key for sessions
  

# Configure JWT
# app.config['JWT_SECRET_KEY'] = 'G0kulTh3GO@T'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
# jwt = JWTManager(app)

# Configure CORS with support for credentials
# Configure CORS with support for credentials
CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],  
        # "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        # "allow_headers": ["Content-Type", "Authorization"],
        # "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})



# Enable logging for CORS
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('flask_cors')
logger.setLevel(logging.DEBUG)

# Debug: Print environment variables
logging.debug(f"DB_USER: {os.getenv('DB_USER')}")
logging.debug(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
logging.debug(f"DB_HOST: {os.getenv('DB_HOST')}")
logging.debug(f"DB_NAME: {os.getenv('DB_NAME')}")
logging.debug(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")

# # Enable logging for CORS
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('flask_cors')
# logger.setLevel(logging.DEBUG)



# Set the secret key for proper session management, otherwise you get a 500 when logging in
# This is a temporary secret key, will need to change this to a more secure key
# app.secret_key = os.getenv('SECRET_KEY')
# app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
# app.config['JWT_COOKIE_SECURE'] = True  # Ensures cookies are only sent over HTTPS
# app.config['JWT_COOKIE_SAMESITE'] = 'None'  # Controls cross-site behavior; try 'Lax' or 'Strict'


# jwt = JWTManager(app)

# Configure CORS (Cross-Origin Resource Sharing) to allow credentials
# This will allow the frontend to send cookies and credentials to the backend
# Grabbinn the frontend URL from the .env file

# CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": os.getenv('FRONTEND_URL')}})

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='None',  # 'None' to allow cross-site cookies
#     SESSION_COOKIE_NAME='pantry_session',
#     PERMANENT_SESSION_LIFETIME=timedelta(days=7)
# )


# Path to groceryapp.sql
sql_file_path = os.path.join("..", "database", "groceryapp.sql")

# Demo Groceries to test functionality
groceries = [
    {"id": 1, "name": "Milk", "quantity": 1},
    {"id": 1, "name": "Eggs", "quantity": 12}
]

USER_NOT_FOUND = {"Error": "User not found"}
CONTENT_NOT_VALID = {"Error": "Invalid request body"}

# MySQL database configuration
# Will need to go though and change values to match our values
#db_config = {
#    'user': os.getenv('DB_USER'),
#    'password': 'password',
#    'host': 'localhost',
#    'database': 'GroceryApp'
#}


# Returns True if content is valid False otherwise
def content_is_valid(content, list_to_be_valid):
    for item in list_to_be_valid:
        if item not in content:
            return False
    return True


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
#def get_db_connection():
#    try:
#        conn = mysql.connector.connect(**db_config)
#        if conn.is_connected():
#            return conn
#    except Error as txt:
#        print(f"Error with database connectionL: {txt}")
#        return None


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

# # Example route to set a session variable
# @app.route('/set_session/<username>')
# def set_session(username):
#     session['username'] = username
#     return jsonify({"message": f"Session set for user {username}"})



#########################################
# Login and Logout functions, both POST #
#########################################
@app.route('/api/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    """
    "Login" depending on return status
    
    user_name and password are passed in body
    
    Returns:
        200 if successful
        400 body content Invalid
        404 user not found
        401 password incorrect
        500 database error
    """
    try:
        content = request.get_json()
        logging.debug(f"Received login request with content: {content}")
        
        if not content_is_valid(content, ['user_name', 'password']):
            logging.debug("Content is not valid")
            return jsonify({"message": "Content not valid"}), 400
            
        conn = get_db_connection()
        if conn is None:
            return jsonify({"Error": "Failed to connect to the database"}), 500

        cursor = conn.cursor(dictionary=True)
       
        user_query = """SELECT user_id AS id, user_name AS username, password as hashed_password
            FROM GroceryApp.Users
            WHERE user_name = %s
            """
        cursor.execute(user_query, (content['user_name'],))
     
        user = cursor.fetchall()
        if not user:
            logging.debug("User not found")
            conn.close()
            return jsonify({"message": "User not found"}), 404
        hashed_password = user[0]['hashed_password']
        
        if bcrypt.check_password_hash(hashed_password, content['password']):
            session["username"] = user[0]['username']
            session["user_id"] = user[0]['id']
            logging.debug("Login successful")
            conn.close()
            return jsonify({'Message': 'Login successful'}), 200
        else:
            logging.debug("Invalid password")
            conn.close()
            return jsonify({'Message': 'Invalid password'}), 401
    except mysql.connector.Error as err:
        logging.error(f"Database error: {err}")
        if conn and conn.is_connected():
            conn.close()
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        if conn and conn.is_connected():
            conn.close()
        return jsonify({"Error": f"An error occurred: {e}"}), 500

    
####################################################################################
# Check if user is logged in for session management                                #
####################################################################################

@app.route('/api/check_login', methods=['GET'])
@cross_origin(supports_credentials=True)
def check_login():
    if 'username' in session:
        return jsonify(logged_in=True, user=session['username']), 200
    else:
        return jsonify(logged_in=False), 200


####################################################################################
# GET, POST, PUT, and DELETE User. Also login via POST and change password via PUT #
####################################################################################
@app.route('/api/<username>', methods=['GET'])
def get_user_info(username):
    """
    Returns user_id, user_name, first_name, last_name, profile_pic_url, email, phone number, SMS notifications preference, email notifications preference, and preferred notification time
   
    username is passed in URL
   
    Returns:
    200 if successful
    404 if user not found
    500 internal server error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
       
        user_query = """SELECT user_id AS id, user_name AS username, first_name, last_name, profile_pic_url, email, phone_number, receive_sms_notifications, receive_email_notifications, preferred_notification_time
            FROM GroceryApp.Users
            WHERE user_name = %s
            """
        cursor.execute(user_query, (username,))
        user = cursor.fetchall()
        if not user:
            conn.close()
            return jsonify(USER_NOT_FOUND), 404
            
        # Handle nullable values
        user = user[0]  # Fetch the first (and only) row
        user['phone_number'] = user['phone_number'] or ''  # Default to empty string
        user['profile_pic_url'] = user['profile_pic_url'] or ''  # Default to empty string
        user['preferred_notification_time'] = str(user['preferred_notification_time']) or ''  # Convert time to string and default to empty string
            
        conn.close()
        return jsonify(user), 200
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/user', methods=['POST'])
def add_user():
    """
    Creates user
   
    User info is passed in body of message.
    Expected:
        user_name (string)
        password (string)
        first_name (string)
        last_name (string)
        profile_pic_url (string)
        email (string)
        phone_number (string)
        receive_sms_notifications (bool)
        receive_email_notifications (bool)
        preferred_notification_time (TIME)
       
    Returns:
        201 if successful
        400 body content Invalid
        409 if user already exists
        500 Internal Server error or database error
    """
    try:
        content = request.get_json()
        
        if not content_is_valid(content, ['user_name', 'password', 'first_name', 'last_name', 'email', 'receive_sms_notifications', 'receive_email_notifications']):
            return jsonify(CONTENT_NOT_VALID), 400
            
        # Provide default values for optional fields
        content['profile_pic_url'] = content.get('profile_pic_url', '')
        content['phone_number'] = content.get('phone_number', '')
        content['preferred_notification_time'] = content.get('preferred_notification_time', None)
            
        hashed_password = bcrypt.generate_password_hash(content['password']).decode('utf-8')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (content['user_name'],))
        user = cursor.fetchone()
        if user:
            conn.close()
            return jsonify({"Error": "User already exists"}), 409
   
        # Insert new grocery item
        insert_query = """
            INSERT INTO Users (user_name, password, first_name, last_name, profile_pic_url, email, phone_number, receive_sms_notifications, receive_email_notifications, preferred_notification_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content['user_name'], hashed_password, content['first_name'], content['last_name'], content['profile_pic_url'], content['email'], content['phone_number'], content['receive_sms_notifications'], content['receive_email_notifications'], content['preferred_notification_time']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "User created successfully"}), 201
       
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/<username>', methods=['PUT'])
def update_user(username):
    """
    Updates user information.

    User info is passed in body of message.
   
    Expected:
        user_name (string) (Passed in URL)

        password (string)
        first_name (string)
        last_name (string)
        profile_pic_url (string)
        email (string)
        phone_number (string)
        receive_sms_notifications (bool)

    Returns:
        200 if successful
        400 body content Invalid
        404 if user not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        content = request.get_json()
        if not content_is_valid(content, ['password', 'first_name', 'last_name', 'email', 'receive_sms_notifications', 'receive_email_notifications']):
            conn.close()
            return jsonify(CONTENT_NOT_VALID), 400
            
        # Provide default values for optional fields
        content['profile_pic_url'] = content.get('profile_pic_url', '')
        content['phone_number'] = content.get('phone_number', '')
        content['preferred_notification_time'] = content.get('preferred_notification_time', None)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (username,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        if not content:
            conn.close()
            return jsonify(CONTENT_NOT_VALID), 400

        update_query = """
            UPDATE GroceryApp.Users
            SET user_name = %s, password = %s, first_name = %s, last_name = %s, profile_pic_url = %s, email = %s, phone_number = %s, receive_sms_notifications = %s, receive_email_notifications = %s, preferred_notification_time = %s
            WHERE user_id = %s
            """
        hashed_password = bcrypt.generate_password_hash(content['password']).decode('utf-8')
        cursor.execute(update_query, (username, hashed_password, content['first_name'], content['last_name'], content['profile_pic_url'], content['email'], content['phone_number'], content['receive_sms_notifications'], content['receive_email_notifications'], content['preferred_notification_time']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/<username>', methods=['DELETE'])
def delete_user(username):
    """
    Deletes a user.
   
    username is passed in URL

    Returns:
        200 if successful
        404 if user not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (username,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        delete_query = "DELETE FROM GroceryApp.Inventory WHERE user_id = %s"
        cursor.execute(delete_query, (user['user_id'],))
       
        delete_query_recipes = "DELETE FROM GroceryApp.Recipes WHERE user_id = %s"
        cursor.execute(delete_query_recipes, (user['user_id'],))

        delete_query_users = "DELETE FROM GroceryApp.Users WHERE user_id = %s"
        cursor.execute(delete_query_users, (user['user_id'],))
       
        conn.commit()
        conn.close()
        return jsonify({"Message": "User deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


################################################################
# GET, POST, PUT, DELETE User's Groceries (in GroceryApp.Inventory) #
################################################################
@app.route('/api/groceries', methods=['GET'])
@jwt_required()
def get_groceries():
    """
    Returns grocery items for the logged-in user.
   
    Returns:
        200 if groceries successfully returned
        401 if user not logged in
        404 if user not found or user has no groceries
        500 Internal Server Error: Database error.
    """   
    try:
        current_user = get_jwt_identity()
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (current_user,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        groceries_query = "SELECT * FROM GroceryApp.Inventory WHERE user_id = %s"
        cursor.execute(groceries_query, (user['user_id'],))
        groceries = cursor.fetchall()
        
        conn.close()
        
        if not groceries:
            return jsonify({"Error": "No groceries found"}), 404
        
        return jsonify(groceries), 200
    except mysql.connector.Error as err:
        # Database error
        print(f"Database error: {err}")
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        print(f"An error occurred: {e}")
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/groceries', methods=['POST'])
def add_grocery():
    """
    Create a new grocery item for the specified user.
    Request Body:
    {
        "food_id": int,
        "quantity": int,
        'user_id': int,
        'location_id: int,
        'expiration_date: date,
        'date_purchase': date,
        'status': ENUM('fresh', 'used', 'spoiled') default fresh
        'category': ENUM('green', 'yellow', 'red') default green
    }
    Returns:
        201 Created: New grocery item created successfully.
        400 Bad Request: Invalid request body.
        404 Not Found: User not found.
        404: food_id not found.
        404: location_id not found.
        500 Internal Server Error: Database error.
    """
    
    content = request.get_json()
    if not content_is_valid(content, ['food_id', 'quantity', 'user_id', 'location_id', 'expiration_date', 'date_purchase', 'status', 'categor']):
        return jsonify(CONTENT_NOT_VALID), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    
        # Check if user id exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_id = %s"
        cursor.execute(user_query, (content['user_id'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
            
        # Check if food id exists
        user_query = "SELECT food_id FROM GroceryApp.AllFoods WHERE food_id = %s"
        cursor.execute(user_query, (content['food_id'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Food ID not found"}), 404
            
        # Check if location id exists
        user_query = "SELECT location_id FROM GroceryApp.Locations WHERE location_id = %s"
        cursor.execute(user_query, (content['location_id'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Location ID not found"}), 404
    
        # Insert new grocery item
        insert_query = """
            INSERT INTO GroceryApp.Inventory (food_id, quantity, user_id, location_id, expiration_date, date_purchase, status, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content['food_id'], content['quantity'], content['user_id'], content['location_id'], content['expiration_date'], content['date_purchase'], content['status'], content['category']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Grocery item created successfully"}), 201
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/groceries/<int:inventory_id>', methods=['PUT'])
def update_grocery(inventory_id):
    """
    Updates an existing grocery item in the inventory for the specified user.

    Inventory ID passed in URL

    Request Body:
    {
        "food_id": int,
        "quantity": int,
        "user_id": int,
        "location_id": int,
        "expiration_date": date,
        "date_purchase": date,
        "status": ENUM('fresh', 'used', 'spoiled'),
        "category": ENUM('green', 'yellow', 'red')
    }

    Returns:
        200 OK: Grocery item updated successfully.
        400 Bad Request: Invalid request body.
        404 Not Found: Inventory item or associated user/food/location not found.
        500 Internal Server Error: Database error.
    """
    
    content = request.get_json()
    if not content_is_valid(content, ['food_id', 'quantity', 'user_id', 'location_id', 'expiration_date', 'date_purchase', 'status', 'category']):
        return jsonify(CONTENT_NOT_VALID), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the inventory item exists
        inventory_query = "SELECT * FROM GroceryApp.Inventory WHERE inventory_id = %s"
        cursor.execute(inventory_query, (inventory_id,))
        inventory_item = cursor.fetchone()
        if not inventory_item:
            conn.close()
            return jsonify({"Error": "Inventory item not found"}), 404

        # Check if the user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_id = %s"
        cursor.execute(user_query, (content['user_id'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        # Check if the food exists
        food_query = "SELECT food_id FROM GroceryApp.AllFoods WHERE food_id = %s"
        cursor.execute(food_query, (content['food_id'],))
        food = cursor.fetchone()
        if not food:
            conn.close()
            return jsonify({"Error": "Food ID not found"}), 404

        # Check if the location exists
        location_query = "SELECT location_id FROM GroceryApp.Locations WHERE location_id = %s"
        cursor.execute(location_query, (content['location_id'],))
        location = cursor.fetchone()
        if not location:
            conn.close()
            return jsonify({"Error": "Location ID not found"}), 404

        # Update the grocery item
        update_query = """
            UPDATE GroceryApp.Inventory
            SET food_id = %s, quantity = %s, user_id = %s, location_id = %s, expiration_date = %s, date_purchase = %s, status = %s, category = %s
            WHERE inventory_id = %s
        """
        cursor.execute(update_query, (
            content['food_id'], content['quantity'], content['user_id'], 
            content['location_id'], content['expiration_date'], content['date_purchase'], 
            content['status'], content['category'], inventory_id
        ))
        
        conn.commit()
        conn.close()
        return jsonify({"Message": "Grocery item updated successfully"}), 200

    except mysql.connector.Error as err:
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 500
        

@app.route('/api/groceries/<username>', methods=['DELETE'])
def delete_grocery(username):
    """
    Deletes a grocery item from GroceryApp.Inventory.
   
    username is passed in URL

    Returns:
        200 if successful
        404 if user not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (username,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
           
        # Delete records from related tables (e.g., Inventory)
        delete_query_inventory = "DELETE FROM GroceryApp.Inventory WHERE user_id = %s"
        cursor.execute(delete_query_inventory, (user['user_id'],))
       
        conn.commit()
        conn.close()
        return jsonify({"Message": "User deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500
       
       
########################################################
# GET, POST, DELETE Food Item (in GroceryApp.AllFoods) #
########################################################
@app.route('/api/<food_item>', methods=['GET'])
def get_food_item(food_name):
    """
    Returns information for specified food item.
   
    food item name (food_name) is passed in URL
   
    Returns:
        200 if food item information successfully returned
        404 if food item not found
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT food_id, food_name, expiration_days, quantity, food_type
            FROM GroceryApp.AllFoods
            WHERE food_name = %s
        """
        cursor.execute(query, (food_name,))  # Comma after username makes it a tuple

        # Check if user exists
        results = cursor.fetchall()
        if not results:
            conn.close()
            return jsonify({"Error": "No food item with that name exists"}), 404

        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/item', methods=['POST'])
def add_food_item():
    """
    Create a new food item
    Request Body:
    {
        "food_name": "string",
        "expiration_days": "int",
        "food_type": "string"
    }
    Returns:
        201 Created: New grocery item created successfully.
        400 Bad Request: Invalid request body.
        500 Internal Server Error: Database error.
    """

    # Get food ID
    data = request.get_json()
    if not content_is_valid(data, ['food_name', 'expiration_days', 'food_type']):
        return jsonify(CONTENT_NOT_VALID), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        insert_query = """
            INSERT INTO GroceryApp.AllFoods (food_name, expiration_days, food_type)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (data['food_name'], data['expiration_days'], data['food_type']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Food item created successfully"}), 201
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/<food_name>', methods=['DELETE'])
def delete_food_item(food_name):
    """
    Deletes a food item.
   
    food item name is passed in URL

    Returns:
        200 if successful
        404 if user not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        user_query = "SELECT food_id FROM GroceryApp.AllFoods WHERE food_name = %s"
        cursor.execute(user_query, (food_name,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
            
        # Delete records from related tables (e.g., Inventory)
        delete_query_inventory = "DELETE FROM GroceryApp.Inventory WHERE food_id = %s"
        cursor.execute(delete_query_inventory, (user['food_id'],))
        
        # Delete records from related table (e.g., Ingredients)
        delete_query_ingredients = "DELETE FROM GroceryApp.Ingredients WHERE food_id = %s"
        cursor.execute(delete_query_ingredients, (user['food_id'],))
        
        delete_query = "DELETE FROM GroceryApp.AllFoods WHERE food_id = %s"
        cursor.execute(delete_query, (user['food_id'],))
       
        conn.commit()
        conn.close()
        return jsonify({"Message": "Food item deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500
        
        
##############################
# GET, POST, DELETE Location #
##############################
@app.route('/api/<location_name>', methods=['GET'])
def get_location(location_name):
    """
    Returns information for location.
   
    location name is passed in URL
   
    Returns:
        200 if location information successfully returned
        404 if location not found
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT location_id, location_name
            FROM GroceryApp.Locations
            WHERE location_name = %s
        """
        cursor.execute(query, (location_name,))  # Comma after username makes it a tuple

        # Check if user exists
        results = cursor.fetchall()
        if not results:
            conn.close()
            return jsonify({"Error": "No location with that name exists"}), 404

        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/location', methods=['POST'])
def add_location():
    """
    Create a new location
    Request Body:
    {
        "location_name": "string",
    }
    Returns:
        201 Created: New location created successfully.
        400 Bad Request: Invalid request body.
        500 Internal Server Error: Database error.
    """
    data = request.get_json()
    if not content_is_valid(data, ['location_name']):
        return jsonify(CONTENT_NOT_VALID), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        insert_query = """
            INSERT INTO GroceryApp.Locations (location_name)
            VALUES (%s)
        """
        cursor.execute(insert_query, (data['location_name'],))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Location item created successfully"}), 201
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/<location_name>', methods=['DELETE'])
def delete_location(location_name):
    """
    Deletes a location item from GroceryApp.Locations.

    location item name is passed in URL

    Returns:
        200 if successful
        404 if location not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT location_id FROM GroceryApp.Locations WHERE location_name = %s"
        cursor.execute(user_query, (location_name,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Location not found"}), 404

        # Delete records from related table (e.g., Inventory)
        delete_query_inventory = "DELETE FROM GroceryApp.Inventory WHERE location_id = %s"
        cursor.execute(delete_query_inventory, (user['location_id'],))

        # Delete records from Locations
        delete_query = "DELETE FROM GroceryApp.Locations WHERE location_id = %s"
        cursor.execute(delete_query, (user['location_id'],))

        conn.commit()
        conn.close()
        return jsonify({"Message": "Location deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


##################################
# GET, POST, DELETE from Recipes #
##################################
@app.route('/api/<recipe_name>', methods=['GET'])
def get_recipe(recipe_name):
    """
    Returns information for recipe.
   
    recipe name is passed in URL
   
    Returns:
        200 if recipe information successfully returned
        404 if recipe not found
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT recipe_id, recipe_name, recipe_url, user_id, recipe_notification
            FROM GroceryApp.Recipes
            WHERE recipe_name = %s
        """
        cursor.execute(query, (recipe_name,))  # Comma after username makes it a tuple

        # Check if user exists
        results = cursor.fetchall()
        if not results:
            conn.close()
            return jsonify({"Error": "No recipe with that name exists"}), 404
            
        # Handle nullable recipe_notification
        results = results[0]
        results['recipe_notification'] = results.get('recipe_notification', None) or ''

        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/recipe', methods=['POST'])
def add_recipe():
    """
    Create a new recipe
    Request Body:
    {
        'recipe_id': int,
        'recipe_name': string,
        'recipe_url': string,
        'user_id': int,
        'recipe_notification': bool
    }
    Returns:
        201 Created: New recipe created successfully.
        400 Bad Request: Invalid request body.
        500 Internal Server Error: Database error.
    """
    data = request.get_json()
    if not content_is_valid(data, ['recipe_name', 'recipe_url', 'user_id']):
        return jsonify(CONTENT_NOT_VALID), 400
        
     # Provide default values for optional fields
    data['recipe_notification'] = data.get('recipe_notification', False)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        insert_query = """
            INSERT INTO GroceryApp.Recipes (recipe_name, recipe_url, user_id, recipe_notification)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (data['recipe_name'], data['recipe_url'], data['user_id'], data['recipe_notification']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Recipe item created successfully"}), 201
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/<recipe_name>', methods=['DELETE'])
def delete_recipe(recipe_name):
    """
    Deletes a recipe item from GroceryApp.Recipes.
   
    recipe item name is passed in URL

    Returns:
        200 if successful
        404 if location not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT recipe_id FROM GroceryApp.Recipes WHERE recipe_name = %s"
        cursor.execute(user_query, (recipe_name,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Location not found"}), 404
        
        # Delete records from related table (e.g., Inventory)
        delete_query_inventory = "DELETE FROM GroceryApp.Ingredients WHERE recipe_id = %s"
        cursor.execute(delete_query_inventory, (user['recipe_id'],))
        
        # Delete records from Locations
        delete_query = "DELETE FROM GroceryApp.Recipes WHERE recipe_id = %s"
        cursor.execute(delete_query, (user['recipe_id'],))
       
        conn.commit()
        conn.close()
        return jsonify({"Message": "Recipe deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500
        
        
######################################
# GET, POST, DELETE from Ingredients #
######################################
@app.route('/api/ingredients/<recipe_id>', methods=['GET'])
def get_ingredients(recipe_id):
    """
    Returns all rows from Ingredients that have recipe_id.
   
    recipe id is passed in URL
   
    Returns:
        200 if recipe rows successfully returned
        404 if recipe rows not found
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT recipe_id, food_id, quantity_required
            FROM GroceryApp.Ingredients
            WHERE recipe_name = %s
        """
        cursor.execute(query, (recipe_id,))  # Comma after username makes it a tuple

        # Check if user exists
        results = cursor.fetchall()
        if not results:
            conn.close()
            return jsonify({"Error": "No ingredients with that recipe_id exist"}), 404

        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/ingredient', methods=['POST'])
def add_ingredient():
    """
    Create a new ingredient
    Request Body:
    {
        'recipe_id': int,
        'food_id': string,
        'quantity_required': string
    }
    Returns:
        201 Created: New ingredient created successfully.
        400 Bad Request: Invalid request body.
        500 Internal Server Error: Database error.
    """
    data = request.get_json()
    if not content_is_valid(data, ['recipe_id', 'food_id', 'quantity_required']):
        return jsonify(CONTENT_NOT_VALID), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        insert_query = """
            INSERT INTO GroceryApp.Ingredients (recipe_id, food_id, quantity_required)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (data['recipe_id'], data['food_id'], data['quantity_required']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Ingredient created successfully"}), 201
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/ingredients/<recipe_id>', methods=['DELETE'])
def delete_ingredient(recipe_id):
    """
    Deletes an ingredient GroceryApp.Ingredients
   
    recipe id is passed in URL

    Returns:
        200 if successful
        404 if location not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT recipe_id FROM GroceryApp.Ingredients WHERE recipe_id = %s"
        cursor.execute(user_query, (recipe_id,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Ingredient not found"}), 404
        
        # Delete records from related table (e.g., Inventory)
        delete_query_inventory = "DELETE FROM GroceryApp.Ingredients WHERE recipe_id = %s"
        cursor.execute(delete_query_inventory, (user['recipe_id'],))
       
        conn.commit()
        conn.close()
        return jsonify({"Message": "Ingredient deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


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