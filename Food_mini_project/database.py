# step 1 . Create database  database.py

import sqlite3
DATABASE_NAME = "food_order.db"

def get_connection():
    '''
    Whenever the application needs to communicate with the database, call this function to get a database connection.
    '''
    connection = sqlite3.connect(DATABASE_NAME)

    return connection # opens a connection to our SQLite database.