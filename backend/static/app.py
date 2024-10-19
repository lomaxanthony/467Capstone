from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)       #Allow frontend to communicate with the backend

# Demo Groceries to test functionality
groceries = [
    {"id": 1, "name": "Milk", "quantity": 1},
    {"id": 1, "name": "Eggs", "quantity": 12}
]

@app.route('/api/groceries', methods=['GET'])
def get_groceries():
    return jsonify(groceries)

@app.route('/api/groceries', methods={'POST'})
def add_grocery():
    new_item = request.json
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
    app.run(debug=True)