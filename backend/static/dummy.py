from datetime import datetime, timedelta

def calc_date(expiration_days):
    # Get today's date
    today = datetime.today()
    
    # Calculate expiration date
    expiration_date = today + timedelta(days=days_to_expiration)
    
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
        'date_purchase': date,`
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
    del content['food_name']
    if not content_is_valid(content, ['food_id', 'quantity', 'expiration_days', 'date_purchase']):
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