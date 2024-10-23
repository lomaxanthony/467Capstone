from flask import Flask, jsonify, request, send_from_directory, redirect, url_for, render_template, session, flash
from flask_cors import CORS
import os
from datetime import timedelta
from google.cloud import datastore

app = Flask(__name__, static_folder='static', static_url_path='')
client = datastore.Client()
CORS(app)       #Allow frontend to communicate with the backend

# Demo Groceries to test functionality
groceries = [
    {"id": 1, "name": "Milk", "quantity": 1},
    {"id": 1, "name": "Eggs", "quantity": 12}
]

# @app.route('/api/<username>/groceries', methods=['GET']) # Added /<username> so we know who's groceries we're taking from
@app.route('/api/groceries', methods=['GET'])
def get_groceries(username):
    return jsonify(groceries)
    
    """query = client.query(kind="grocery")
    query.add_filter('username', '=', username)
    results = list(query.fetch())
    for r in results:
        r['id'] = r.key.id
    return (results, 200)"""

    # return jsonify(groceries)

# @app.route('/api/<username>/groceries', methods={'POST'}) # Added /<username> so we know who's groceries we're adding to
@app.route('/api/groceries', methods={'POST'})
def add_grocery(username):
    new_item = request.json()
    groceries.append(new_item)
    return jsonify(new_item), 201
    
    """content = request.json()
    new_grocery_item = datastore.Entity(key=client.key("grocery")) # Stores it as a kind "Grocery"
    if "name" not in content or "quantity" not in content:
        return ({"Error": "The request body is missing at least one of the required attributes"}, 400)
    new_grocery_item.update({
        "username": content[username],
        "name": content["name"],
        "quantity": content["quantity"]
    })
    client.put(new_grocery_item)
    new_grocery_item['id'] = new_grocery_item.key.id
    return (new_grocery_item, 201)"""

    # new_item = request.json()
    # groceries.append(new_item)
    # return jsonify(new_item), 201

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    # Serve Vue frontend files
    if path != "" and os.path.exists(f"static/{path}"):
        return send_from_directory('static', path)
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
