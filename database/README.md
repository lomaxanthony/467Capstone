# GroceryApp - Smart Grocery Management database

## Overview

GroceryApp is a smart grocery management tool designed to help users track their groceries, get notified about items nearing expiration, and find recipes to use up ingredients before they spoil. This database aims to store the users needed information and modify it all from the website. 

## Features

- **Inventory Management**: Record groceries with expiration dates, quantities, and locations.
- **Expiration Notifications**: Receive notifications (via email or SMS) when items are nearing expiration or have expired.
- **Recipe Suggestions**: Find recipes that use ingredients that are nearing expiration to minimize food waste.
- **Location Tracking**: Organize groceries by storage location (e.g., Fridge, Freezer, Pantry).
- **User Preferences**: Customize notification settings for email or SMS alerts.

## Database Setup

### Prerequisites

- MySQL or Google Cloud SQL
- Google Cloud account with Google Cloud SQL setup (if using cloud database)

### Setting Up the Database

1. **Import the SQL Script**
    - The SQL script to create the database can be found in the `database` directory.
    - import the script into Google Cloud SQL:
        - Upload the `GroceryApp.sql` file to a Google Cloud Storage bucket.
        - Use the Google Cloud SQL Console to import the file from Cloud Storage.

2. **Database Schema**
   - The `GroceryApp.sql` file contains the schema to create the following tables:
     - `Users`: Stores user information such as user name, email, and phone number.
     - `AllFoods`: Catalog of available food types.
     - `Locations`: Stores different storage locations for food items.
     - `Inventory`: Tracks the food items owned by users, including expiration information.
     - `Recipes`: Stores recipe details, including URLs for reference.
     - `Ingredients`: Stores ingredients required for recipes.
     - `UserPreferences`: Stores user preferences for notifications.

3. **Environment Variables for Database Connection - IN Progress**
   - Create a `.env` file with the following variables:
     ```
     DB_HOST
     DB_USER
     DB_PASSWORD
     DB_NAME
     ```



Feel free to reach out if you have questions or want to learn more about the project!
