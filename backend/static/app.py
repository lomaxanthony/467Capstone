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

USER_NOT_FOUND = {"Error": "User not found"}
CONTENT_NOT_VALID = {"Error": "Invalid request body"}

# MySQL database configuration
# Will need to go though and change values to match our values
db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'database': 'GroceryApp'
}


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


###################################
# GET, POST, PUT, and DELETE User #
###################################
@app.route('/api/<username>', methods=['GET'])
def get_user_info(username):
    """
    Returns user_id, user_name, email, phone number, and SMS notifications preference
   
    username is passed in URL
   
    Returns:
    200 if successful
    404 if user not found
    500 internal server error
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
       
        user_query = """SELECT user_id AS id, user_name AS username, email, phone_number, receive_sms_notifications, receive_email_notifications, preferred_notification_time
            FROM GroceryyApp.Users
            WHERE user_name = %s
            """
            cursor.execute(user_query, (usuername))
            user = cursor.fetchall()
            if not user:
                conn.close()
                return jsonify(USER_NOT_FOUND), 404
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
        email (string)
        phone_number (string)
        receive_sms_notifications (bool)
       
    Returns:
        201 if successful
        400 body content Invalid
        409 if user already exists
        500 Internal Server error or database error
    """
    try:
        content = request.get_json()
        
        if not content_is_valid(content, ['user_name', 'email', 'phone_number', 'receive_sms_notifications', 'receive_email_notifications', 'preferred_notification_time'])
            return jsonify(CONTENT_NOT_VALID), 400
        
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
            INSERT INTO Users (user_name, email, phone_number, receive_sms_notifications, receive_email_notifications, preferred_notification_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (content['user_name'], content['email'], content['phone_number'], content['receive_sms_notifications'], content['receive_email_notifications'], content['preferred_notification_time']))
        conn.commit()
        conn.close()
        return jsonify({"Message": "User created successfully"}), 201
       
    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500


@app.route('/api/user', methods=['PUT'])
def update_user(username):
    """
    Updates user information.

    User info is passed in body of message.
   
    Expected:
        user_name (string)
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
        if not content_is_valid(content, ['user_name', 'email', 'phone_number', 'receive_sms_notifications', 'receive_email_notifications', 'preferred_notification_time']):
            conn.close()
            return jsonify(CONTENT_NOT_VALID), 400

        user_query = "SELECT user_id FROM GroceryApp.Users WHERE user_name = %s"
        cursor.execute(user_query, (content['user_name',))
        user = cursor.fetchone()
        if not user:
            conn.close()
            return jsonify({"Error": "User not found"}), 404

        content = request.get_json()
        if not content:
            conn.close()
            return jsonify(CONTENT_NOT_VALID), 400

        update_query = """
            UPDATE GroceryApp.Users
            SET user_name = %s, email = %s, phone_number = %s, receive_sms_notifications = %s, receive_email_notifications = %s, preferred_notification_time = %s
            WHERE user_id = %s
        """
        cursor.execute(update_query, (content['user_name'], content['email'], content['phone_number'], content['receive_sms_notifications'], user['user_id'], user['receive_email_notifications'], user['preferred_notification_time']))
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
# GET, POST, DELETE User's Groceries (in GroceryApp.Inventory) #
################################################################
@app.route('/api/groceries/<username>', methods=['GET'])
def get_groceries(username):
     """
    Returns grocery items for the specified user.
   
    username is passed in URL
   
    Returns:
        200 if groceries successfully returned
        404 if user not found or user has no groceries
        500 Internal Server Error: Database error.
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

        query = """
            SELECT i.inventory_id AS id, f.food_name AS name, i.quantity
            FROM GroceryApp.Inventory i
            JOIN GroceryApp.Users u ON i.user_id = u.user_id
            JOIN GroceryApp.AllFoods f ON i.food_id = f.food_id
            WHERE u.user_name = %s
        """
        cursor.execute(query, (username,))  # Comma after username makes it a tuple

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
        

@app.route('/api/groceries/<username>', methods=['DELETE'])
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


@app.route('/api/<food_name>', methods=['POST'])
def add_food_item(food_name):
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
def delete_user(food_name):
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
def add_location(location_name):
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
        cursor.execute(insert_query, (data['location_name']))
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
def get_location(location_name):
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

        conn.close()
        return jsonify(results), 200

    except mysql.connector.Error as err:
        # Database error
        return jsonify({"Error": f"Database error: {err}"}), 500
    except Exception as e:
        # General error
        return jsonify({"Error": f"An error occurred: {e}"}), 500

@app.route('/api/recipe', methods=['POST'])
def add_recipe(location_name):
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
    if not content_is_valid(data, ['recipe_name', 'recipe_url', 'user_id', 'recipe_notification']):
        return jsonify(CONTENT_NOT_VALID), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        insert_query = """
            INSERT INTO GroceryApp.Recipes (recipe_name, recipe_url, user_id, recipe_notification)
            VALUES (%s)
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
def add_ingredient(location_name):
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
            VALUES (%s)
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
def delete_ingredient(ingredient_name):
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
