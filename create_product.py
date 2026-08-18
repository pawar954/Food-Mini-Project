# create_product.py

import sqlite3
from database import get_connection

def add_product(product_name, price):

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO products (product_name, price)
            VALUES (?, ?)
        """, (product_name, price))

        connection.commit()
        product_id = cursor.lastrowid

        return product_id
    except Exception as e:

        connection.rollback()

        print(f"Product creation failed: {e}")

        return None
    finally:

        connection.close()



# ==================================================================

# GET PRODUCT ID


def get_product_id(product_name):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT product_id

            FROM products

            WHERE product_name = ?
        """, (product_name.strip(),))

        result = cursor.fetchone()

        if result is None:

            print("Product does not exist.")

            return None

        return result[0]

    finally:

        connection.close()


# ============================================================
# GET ALL PRODUCTS


def get_all_products():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                product_id,
                product_name,
                price

            FROM products

            ORDER BY product_id
        """)

        return cursor.fetchall()

    finally:

        connection.close()

