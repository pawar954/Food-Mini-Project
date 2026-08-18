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


# GET CUSTOMER


def get_customer(customer_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                customer_id,
                customer_name,
                email

            FROM customers

            WHERE customer_id = ?
        """, (customer_id,))

        return cursor.fetchone()

    finally:

        connection.close()

