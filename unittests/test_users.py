import unittest
import json
import sys
import os

# Connection to app.py and db_config.py files
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/static')))
from app import app
from db_config import get_db_connection

class DatabaseUserAPI(unittest.TestCase):
    # Set up the test client and initialize testing variables.
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.added_user_ids = []

    # Clean up only the users created during the tests
    def tearDown(self):
        if self.added_user_ids:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.executemany("DELETE FROM GroceryApp.Users WHERE user_id = %s", [(user_id,) for user_id in self.added_user_ids])
            conn.commit()
            conn.close()

    # Test @app.route('/api/<username>', methods=['PUT']) def update_user(username):
    def test_add_user(self):
        user_data = {
            "user_name": "test_user",
            "password": "12345*",
            "first_name": "Jane",
            "last_name": "Doe",
            "profile_pic_url": "http://example.com/profile.jpg",
            "email": "test_user@example.com",
            "phone_number": "1234567890",
            "receive_sms_notifications": True,
            "receive_email_notifications": False,
            "preferred_notification_time": "10:00:00"
        }
        response = self.app.post('/api/user', data=json.dumps(user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User created successfully', response.data)

        # Verify user is present in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM GroceryApp.Users WHERE user_name = %s", (user_data['user_name'],))
        user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user['user_name'], user_data['user_name'])
        self.added_user_ids.append(user['user_id'])  
        conn.close()

    # Test @app.route('/api/<username>', methods=['GET']) def get_user_info(username):
    def test_get_user_info(self):
        # Adds test user function
        self.test_add_user()

        # Gets test user info
        response = self.app.get('/api/test_user')
        self.assertEqual(response.status_code, 200)
        user = json.loads(response.data)
        self.assertEqual(user['username'], 'test_user')
        self.assertEqual(user['email'], 'test_user@example.com')


    # Test @app.route('/api/login', methods=['POST']) def login():
    def test_login_user(self):
        # Adds test user function
        self.test_add_user()

        # Now attempt to log in with correct credentials
        login_data = {
            "user_name": "test_user",
            "password": "12345*"
        }
        response = self.app.post('/api/login', data=json.dumps(login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

        # log in with incorrect credentials
        incorrect_login_data = {
            "user_name": "test_user",
            "password": "wrong_password"
        }
        response = self.app.post('/api/login', data=json.dumps(incorrect_login_data), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid password', response.data)

    # Test @app.route('/api/<username>', methods=['PUT']) def update_user(username):
    def test_update_user(self):
        # Adds test user function
        self.test_add_user()

        # Update the user 
        update_data = {
            "email": "test_user_updated@example.com",
            "phone_number": "9876543210",
            "receive_sms_notifications": False,
            "receive_email_notifications": True,
            "preferred_notification_time": "11:00:00"
        }

        # Send PUT request to update the user
        response = self.app.put('/api/test_user', data=json.dumps(update_data), content_type='application/json')

        print(f"Update Response Status: {response.status_code}")
        print(f"Update Response Data: {response.data.decode()}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User updated successfully', response.data)

        # Verify the update in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM GroceryApp.Users WHERE user_name = %s", ('test_user',))
        user = cursor.fetchone()

        self.assertIsNotNone(user)
        self.assertEqual(user['email'], 'test_user_updated@example.com')
        self.assertEqual(user['phone_number'], '9876543210')
        conn.close()

    # Test @app.route('/api/<username>', methods=['DELETE']) def delete_user(username):
    def test_delete_user(self):
        # Adds test user function
        self.test_add_user()

        # Delete the user
        response = self.app.delete('/api/test_user')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User deleted successfully', response.data)

        # Verify the user no longer exists in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM GroceryApp.Users WHERE user_name = %s", ('test_user',))
        user = cursor.fetchone()
        self.assertIsNone(user)
        conn.close()

if __name__ == '__main__':
    unittest.main()
