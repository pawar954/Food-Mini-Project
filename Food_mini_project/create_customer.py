# 4.1 create_customer.py
import sqlite3
from database import get_connection

def add_customer(name, phone, email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO customers (name, phone, email)
        VALUES (?, ?, ?)
    """, (name, phone, email))

    connection.commit()

    customer_id = cursor.lastrowid

    connection.close()

    return customer_id
# ====================================================================================================