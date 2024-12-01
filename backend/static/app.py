from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template, session, flash
from flask_cors import CORS, cross_origin
from flask_session import Session
from flask_bcrypt import Bcrypt
import mysql.connector
from mysql.connector import Error
import os
import sys
import json
from db_config import get_db_connection
from datetime import timedelta
from google.cloud import vision
from datetime import datetime, timedelta


app = Flask(__name__, static_folder='../../frontend/dist', static_url_path='')
app.config["SECRET_KEY"] = "N3Cr0n_$uPr3mA¢Y"

CORS(app, supports_credentials=True, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],  # Your Vue.js development server
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True
    }
})    #Allow frontend to communicate with the backend
bcrypt = Bcrypt(app) # For hashing password
# vision_client = vision.ImageAnnotatorClient() # For image recognition via google vision

# Ensure session cookies are correctly set
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(days=7)  
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


# Path to groceryapp.sql
sql_file_path = os.path.join("..", "database", "groceryapp.sql")

# Demo Groceries to test functionalit
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


# Returns True if content is valid False otherwise
def content_is_valid(content, list_to_be_valid, optional_fields=None):
    if list_to_be_valid is None:
        list_to_be_valid = []
    if optional_fields is None:
        optional_fields = []

    # Ensure all required fields are present
    for field in list_to_be_valid:
        if field not in content:
            return False

    # Ensure no unexpected fields are present
    allowed_fields = set(list_to_be_valid + optional_fields)
    for key in content.keys():
        if key not in allowed_fields:
            return False

    return True


# # Reads and executes SQL commands from groceryapp.sql
# def execute_sql_file(connection, sql_file_path):
#     with open(sql_file_path, 'r') as file:
#         sql_script = file.read()  # Read the entire file as a single string
#     cursor = connection.cursor()
#     try:
#         cursor.execute(sql_script, multi=True)  # Execute multiple statements at once
#         connection.commit()
#     except Error as e:
#         print(f"Error executing SQL script: {e}")
#     finally:
#         cursor.close()


# def execute_sql_file(connection, sql_file_path):
#     with open(sql_file_path, 'r') as file:
#         sql_commands = file.read().split(';')
    
#     cursor = connection.cursor()
#     for command in sql_commands:
#         if command.strip():
#             cursor.execute(command)
#             connection.commit()  # Commit after each command to ensure sync

#     cursor.close()


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

############################################################
# Route to recognize grocery items using Google Vision API #
############################################################
@app.route('/api/recognize', methods=['POST'])
def recognize_image():
    """
    Recognizes grocery items from an uploaded image using Google Vision API.
    
    Returns:
        200 if successful with recognized labels
        400 if the request is invalid
        500 for internal server errors
    """
    try:
        if 'image' not in request.files:
            return jsonify({"Error": "No image file provided"}), 400
        
        # Get the uploaded image file
        image_file = request.files['image']

        # Google vision expects image in form of bytes
        image_bytes = image_file.read()

        # Create an image object for Google Vision API
        image = vision.Image(content=image_bytes)

        # Use the Vision API to detect labels
        response = vision_client.label_detection(image=image, max_results=3)

        if response.error.message:
            return jsonify({"Error": response.error.message}), 500

        # Extract labels from the response
        labels = [label.description for label in response.label_annotations]
        return jsonify({"recognized_items": labels}), 200

    except Exception as e:
        return jsonify({"Error": f"An error occurred in recognize_image(): {str(e)}"}), 500

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
        
        if not content_is_valid(content, ['user_name', 'password']):
            return jsonify(CONTENT_NOT_VALID), 400
            
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
       
        user_query = """SELECT user_id AS id, user_name AS username, password as hashed_password
            FROM GroceryApp.Users
            WHERE user_name = %s
            """
        cursor.execute(user_query, (content['user_name'],))
     
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify(USER_NOT_FOUND), 404
        hashed_password = user['hashed_password']
        conn.close()
        
        if bcrypt.check_password_hash(hashed_password, content['password']):
            session["username"] = content['user_name']
            return jsonify({'Message': 'Login successful'})
        else:
            return jsonify({'Message': 'Invalid password'}), 401
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """
    Logout by removing username from session
    
    Returns:
        200 if successful
        401 user not logged in
        500 server error
    """
    try:
        if 'username' not in session:
            return jsonify({'Message': 'You are not logged in'}), 401
        
        session.pop('username', None)
        return jsonify({'Message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 500

###################################
# GET, POST, PUT, and DELETE User #
###################################
@app.route('/api/session', methods=['GET'])
@cross_origin(supports_credentials=True)
def check_session():
    """
    Check if the user is logged in by verifying the session.
    Returns:
        200 OK: User is logged in.
        401 Unauthorized: User is not logged in.
    """
    try:
        if 'username' in session:
            return jsonify({"logged_in": True, "username": session['username']}), 200
        else:
            return jsonify({"logged_in": False}), 401
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/user', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_user_info():
    """
    Returns user_id, user_name, first_name, last_name, profile_pic_url, email, phone number, SMS notifications preference, email notifications preference, and preferred notification time
   
    username is given by session
   
    Returns:
    200 if successful
    404 if user not found
    500 internal server error
    """
    try:
        username = session.get("username")
        if not username:
            return jsonify({"Error": "No active session"}), 401

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
       
        user_query = """SELECT user_id AS id, user_name AS username, first_name, last_name, profile_pic_url, email, phone_number, receive_sms_notifications, receive_email_notifications, preferred_notification_time
            FROM GroceryApp.Users
            WHERE user_name = %s
            """
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return jsonify(USER_NOT_FOUND), 404
        conn.close()
        for key, value in user.items():
            if isinstance(value, timedelta):
                user[key] = str(value)
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
    Creates user, no need to login immediately after user creation
   
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
        

        if not content_is_valid(content, ['user_name', 'password', 'first_name', 'last_name', 'email', 'receive_sms_notifications', 'receive_email_notifications'], ['phone_number', 'profile_pic_url', 'preferred_notification_time']):
            return jsonify(CONTENT_NOT_VALID), 400
        
        hashed_password = bcrypt.generate_password_hash(content['password']).decode('utf-8')


        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (content['user_name'],))
        user = cursor.fetchone()
        if user:
            conn.close()
            return jsonify({"Error": "User already exists"}), 409
   
        # Insert new user
        insert_query = """
            INSERT INTO Users (user_name, password, first_name, last_name, profile_pic_url, email, phone_number, receive_sms_notifications, receive_email_notifications, preferred_notification_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content['user_name'], hashed_password, content['first_name'], content['last_name'], content.get('profile_pic_url'), content['email'], content.get('phone_number'), content['receive_sms_notifications'], content['receive_email_notifications'], content.get('preferred_notification_time')))
        conn.commit()
        conn.close()
        session['username'] = content['user_name']
        return jsonify({"Message": "User created successfully"}), 201
       
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/user', methods=['PUT'])
def update_user():
    """
    Updates user information.

    User info is passed in body of message.
   
    Expected (not all required):
        username (string)
        password (string)
        first_name (string)
        last_name (string)
        profile_pic_url (string)
        email (string)
        phone_number (string)
        receive_sms_notifications (bool)
        preferred_notification_time (TIME)

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

        if not content_is_valid(content, [], ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'receive_sms_notifications', 'receive_email_notifications', 'preferred_notification_time']):
            conn.close()
            return jsonify(CONTENT_NOT_VALID), 400

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        if not content:
            conn.close()
            return jsonify(CONTENT_NOT_VALID), 400

        update_fields = []
        update_values = []
        for item in content:
            if item in ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'receive_sms_notifications', 'receive_email_notifications', 'preferred_notification_time']:
                if item == 'password':
                    hashed_password = bcrypt.generate_password_hash(content[item]).decode('utf-8')
                    update_fields.append(f"{item} = %s")
                    update_values.append(hashed_password)
                elif item == 'username':
                    session['username'] = content['username']
                    update_fields.append(f"{item} = %s")
                    update_values.append(session['username'])
                else:
                    update_fields.append(f"{item} = %s")
                    update_values.append(content[item])

        if not update_fields:
            return jsonify({"Error": "None valid fields for update"}), 400

        update_values.append(user['user_id'])

        update_query = f"""
            UPDATE GroceryApp.Users
            SET {', '.join(update_fields)}
            WHERE user_id = %s
            """
        cursor.execute(update_query, update_values)
        conn.commit()
        conn.close()
        return jsonify({"Message": "User updated successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/user', methods=['DELETE'])
def delete_user():
    """
    Deletes a user.
   
    username is taken from session

    Returns:
        200 if successful
        404 if user not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
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

        delete_query_userusage = "DELETE FROM GroceryApp.UserUsage WHERE user_id = %s"
        cursor.execute(delete_query_userusage, (user['user_id'],))
       
        conn.commit()
        conn.close()
        session.pop('username', None)
        return jsonify({"Message": "User deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


#####################################################################
# GET, POST, PUT, DELETE User's Groceries (in GroceryApp.Inventory) #
#####################################################################
@app.route('/api/groceries', methods=['GET'])
def get_groceries():
    """
    Returns grocery items for the specified user.
   
    username is passed in session
   
    Returns:
        200 if groceries successfully returned
        404 if user not found or user has no groceries
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        query = """
            SELECT i.inventory_id AS id, f.food_name AS name, i.quantity
            FROM GroceryApp.Inventory i
            JOIN GroceryApp.Users u ON i.user_id = u.user_id
            JOIN GroceryApp.AllFoods f ON i.food_id = f.food_id
            WHERE u.user_name = %s
        """
        cursor.execute(query, (session['username'],))  # Comma after username makes it a tuple

        # Check if user exists
        results = cursor.fetchall()
        if not results:
            conn.close()
            return jsonify({"Error": "No groceries"}), 404

        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


def calc_date(expiration_days):
    # Get today's date
    today = datetime.today()
    
    # Calculate expiration date
    expiration_date = today + timedelta(days=expiration_days)
    
    # Return expiration date in a readable format (YYYY-MM-DD)
    return expiration_date.strftime('%Y-%m-%d')


@app.route('/api/groceries', methods=['POST'])
def add_grocery():
    """
    Create a new grocery item for the specified user.
    Request Body:
    {
        "food_id": int,
        "quantity": int,
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
        500 Internal Server Error: Database error.
    """
    
    
    content = request.get_json()
    if not content_is_valid(content, ['food_id', 'quantity', 'expiration_days', 'date_purchase', 'food_name']):
        print('Content is not valid')
        return jsonify(CONTENT_NOT_VALID), 400

    content['expiration_date'] = calc_date(content['expiration_days'])
    del content['expiration_days']
                
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    
        # Check if user id exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
        user_id = user['user_id']  # Store the user ID
            
        # Check if food id exists
        user_query = "SELECT food_id FROM GroceryApp.AllFoods WHERE food_id = %s"
        cursor.execute(user_query, (content['food_id'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Food ID not found"}), 404
    
        # Insert new grocery item
        insert_query = """
            INSERT INTO GroceryApp.Inventory (food_id, quantity, user_id, expiration_date, date_purchase)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content['food_id'], content['quantity'], user_id, content['expiration_date'], content['date_purchase']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Grocery item created successfully"}), 201
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/groceries', methods=['PUT'])
def update_grocery():
    """
    Updates an existing grocery item in the inventory for the specified user.

    Request Body:
    {
        'inventory_id': int,
        "food_id": int,
        "quantity": int,
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
    if not content_is_valid(content, ['inventory_id', 'food_id', 'quantity', 'location_id', 'expiration_date', 'date_purchase', 'status', 'category']):
        return jsonify(CONTENT_NOT_VALID), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if the inventory item exists
        inventory_query = "SELECT * FROM GroceryApp.Inventory WHERE inventory_id = %s"
        cursor.execute(inventory_query, (content['inventory_id'],))
        inventory_item = cursor.fetchone()
        if not inventory_item:
            conn.close()
            return jsonify({"Error": "Inventory item not found"}), 404

        # Check if the user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
        user_id = user['user_id']  # Store the user ID
        

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
            content['food_id'], content['quantity'], user_id, 
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


@app.route('/api/groceries', methods=['DELETE'])
def delete_grocery():
    """
    Deletes a specific grocery item from GroceryApp.Inventory.
    
    username is passed in session
    grocery_id is passed in URL parameters

    Returns:
        200 if successful
        404 if user not found or grocery item not found
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        # Check if grocery item exists and belongs to user
        grocery_query = "SELECT * FROM GroceryApp.Inventory WHERE user_id = %s AND grocery_id = %s"
        cursor.execute(grocery_query, (user['user_id'], grocery_id))
        grocery = cursor.fetchone()
        if not grocery:
            conn.close()
            return jsonify({"Error": "Grocery item not found"}), 404

        # Delete grocery item
        delete_query = "DELETE FROM GroceryApp.Inventory WHERE user_id = %s AND grocery_id = %s"
        cursor.execute(delete_query, (user['user_id'], grocery_id))

        conn.commit()
        conn.close()
        return jsonify({"Message": "Grocery item deleted successfully"}), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500
       
       
########################################################
# GET, POST, DELETE Food Item (in GroceryApp.AllFoods) #
########################################################
@app.route('/api/<food_name>', methods=['GET'])
def get_food_item(food_name):
    """
    Returns information for specified food item.
   
    food item name (food_name) is passed in URL
   
    Returns:
        200 if food item information successfully returned
        404 if food item not found
        500 Internal Server Error: Database error.
    """
    print('\nThis is the food name:', food_name)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT food_id, food_name, expiration_days, food_type
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
        "food_type": "string",
        'recipe_id': 'string'
    }
    Returns:
        201 Created: New grocery item created successfully.
        400 Bad Request: Invalid request body.
        404 recipe_id not found
        500 Internal Server Error: Database error.
    """

    # Get food ID
    data = request.get_json()
    if not content_is_valid(data, ['food_name', 'expiration_days', 'food_type', 'recipe_id']):
        return jsonify(CONTENT_NOT_VALID), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if recipe ID exists
        recipe_query = "SELECT recipe_id FROM GroceryApp.Recipes WHERE recipe_id = %s"
        cursor.execute(recipe_query, (data['recipe_id'],))
        recipe = cursor.fetchone()
        if not recipe:
            conn.close()
            return jsonify({"Error": "Recipe ID not found"}), 404
        
        insert_query = """
            INSERT INTO GroceryApp.AllFoods (food_name, expiration_days, food_type, 'recipe_id')
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (data['food_name'], data['expiration_days'], data['food_type'], data['recipe_id']))
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

        # Delete records from related table (e.g., UserUsage)
        delete_query_userusage = "DELETE FROM GroceryApp.UserUsage WHERE food_id = %s"
        cursor.execute(delete_query_userusage, (user['food_id'],))
        
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
        404 if location or user not found
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)


        # Check if the user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
        user_id = user['user_id']  # Store the user ID
        
        query = """
            SELECT location_id, location_name
            FROM GroceryApp.Locations
            WHERE location_name = %s AND user_id = %s
        """
        cursor.execute(query, (location_name, user_id))  # Comma after username makes it a tuple

        # Check if location exists
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

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """
    Returns all location information for the current user.
    
    Returns:
        200 if location information successfully returned
        404 if user not found
        500 Internal Server Error: Database error.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
        user_id = user['user_id']

        query = """
            SELECT location_id, location_name
            FROM GroceryApp.Locations
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))

        results = cursor.fetchall()
        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/location', methods=['POST'])
def add_location():
    """
    Create a new location

    user_id taken from username in session
    
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

        # Check if user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
        user_id = user['user_id']
        
        insert_query = """
            INSERT INTO GroceryApp.Locations (location_name, user_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (data['location_name'], user_id))
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

        # Check if user exists
        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (session['username'],))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404
        user_id = user['user_id']

        user_query = "SELECT location_id FROM GroceryApp.Locations WHERE location_name = %s AND user_id = %s"
        cursor.execute(user_query, (location_name, user_id))
        location = cursor.fetchone()
        if not location:
            conn.close()
            return jsonify({"Error": "Location not found"}), 404

        # Delete records from related table (e.g., Inventory)
        delete_query_inventory = "DELETE FROM GroceryApp.Inventory WHERE location_id = %s"
        cursor.execute(delete_query_inventory, (location['location_id'],))

        # Delete records from Locations
        delete_query = "DELETE FROM GroceryApp.Locations WHERE location_id = %s"
        cursor.execute(delete_query, (location['location_id'],))

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
            SELECT recipe_id, recipe_name
            FROM GroceryApp.Recipes
            WHERE recipe_name = %s
        """
        cursor.execute(query, (recipe_name,))  # Comma after username makes it a tuple

        # Check if recipe exists
        results = cursor.fetchall()
        if not results:
            conn.close()
            return jsonify({"Error": "No recipe with that name exists"}), 404

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
        'recipe_name': string,
        'recipe_url': string
    }
    Returns:
        201 Created: New recipe created successfully.
        400 Bad Request: Invalid request body.
        500 Internal Server Error: Database error.
    """
    data = request.get_json()
    if not content_is_valid(data, ['recipe_name', 'recipe_url']):
        return jsonify(CONTENT_NOT_VALID), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        insert_query = """
            INSERT INTO GroceryApp.Recipes (recipe_name, recipe_url)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (data['recipe_name'], data['recipe_url']))
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

        recipe_query = "SELECT recipe_id FROM GroceryApp.Recipes WHERE recipe_name = %s"
        cursor.execute(recipe_query, (recipe_name,))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "Location not found"}), 404
        
        # Delete records from related table (e.g., Ingredients)
        delete_query_ingredients = "DELETE FROM GroceryApp.Ingredients WHERE recipe_id = %s"
        cursor.execute(delete_query_ingredients, (user['recipe_id'],))
        
        # Delete records from Recipes
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
   
    recipe_id is passed in URL
   
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

#######################################
# Two POSTs and one GET for UserUsage #
#######################################
@app.route('/api/use', methods=['POST'])
def add_use():
    """
    Creates UserUsage instance if instance does not already exist and sets times_used to 1. If instance does exist, adds 1 to times_used.
   
    Expected:
        user_id (int)
        food_id (int)
       
    Returns:
        201 if successful
        400 body content Invalid
        500 Internal Server error or database error
    """
    try:
        content = request.get_json()
        

        if not content_is_valid(content, ['user_id', 'food_id']):
            return jsonify(CONTENT_NOT_VALID), 400
        

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Insert or update usage
        insert_query = """
            INSERT INTO UserUsage (user_id, food_id, times_used)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE times_used = times_used + 1
        """
        cursor.execute(insert_query, (content['user_id'], content['food_id']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Use added successfully"}), 201
       
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/spoil', methods=['POST'])
def add_spoil():
    """
    Creates UserUsage instance if instance does not already exist and sets times_spoiled to 1. If instance does exist, adds 1 to times_spoiled.
   
    Expected:
        user_id (int)
        food_id (int)
       
    Returns:
        201 if successful
        400 body content Invalid
        500 Internal Server error or database error
    """
    try:
        content = request.get_json()
        

        if not content_is_valid(content, ['user_id', 'food_id']):
            return jsonify(CONTENT_NOT_VALID), 400
        

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Insert or update usage
        insert_query = """
            INSERT INTO UserUsage (user_id, food_id, times_spoiled)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE times_spoiled = times_spoiled + 1
        """
        cursor.execute(insert_query, (content['user_id'], content['food_id']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "Spoil added successfully"}), 201
       
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/suggestions/<user_name>', methods=['GET'])
def get_suggestions(user_name):
    """
    Retrieves top 5 spoiled and used foods for the given user.
   
    Expected: user_name passed in URL
       
    Returns:
        200 if successful
        404 user has no instances of UserUsage
        500 Internal Server error or database error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            (
              SELECT 
                food_id,
                times_spoiled,
                'spoiled' as type
              FROM 
                UserUsage
              WHERE user_id = (SELECT user_id FROM Users WHERE user_name = %s)
              ORDER BY 
                times_spoiled DESC
              LIMIT 5
            )
            UNION ALL
            (
              SELECT 
                food_id,
                times_used,
                'used' as type
              FROM 
                UserUsage
              WHERE user_id = (SELECT user_id FROM Users WHERE user_name = %s)
              ORDER BY 
                times_used DESC
              LIMIT 5
            )
        """
        cursor.execute(query, (user_name, user_name))
        result = cursor.fetchall()
        
        if not result:
            conn.close()
            return jsonify({"Error": "No suggestions found"}), 404
        
        top_spoiled = [item for item in result if item['type'] == 'spoiled'] # List comprehension
        top_used = [item for item in result if item['type'] == 'used']
        
        conn.close()
        return jsonify({
            "top_spoiled": top_spoiled,
            "top_used": top_used
        }), 200
       
    except mysql.connector.Error as err:
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({"Error": f"An error occurred: {e}"}), 500


# Serve the Vue.js frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Initialize the database connection
    conn = get_db_connection()

    # Specify the path to the groceryapp.sql file
    sql_file_path = '../../database/GroceryApp.sql'  # Adjust this path as needed

    # Call the function to execute the SQL file
    # execute_sql_file(conn, sql_file_path)

    # Close the connection
    conn.close()

    app.run(debug=True)