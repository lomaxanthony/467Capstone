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
    if not content_is_valid(content, ['food_name', 'food_id', 'quantity', 'expiration_days', 'date_purchase']):
        return jsonify(CONTENT_NOT_VALID), 400

    content['expiration_date'] = calc_date(content['expiration_days'])
    del content['expiration_days']

    try:
        content['date_purchase'] = datetime.strptime(content['date_purchase'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"Error": "Invalid date format for date_purchase"}), 400

    #Ensure expiration_date is in date format (YYYY-MM-DD)
    try:
        content['expiration_date'] = datetime.strptime(content['expiration_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"Error": "Invalid date format for expiration_date"}), 400