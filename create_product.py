import sqlite3

from database import get_connection


# ============================================================
# Add Product
# ============================================================
def add_product(product_name, price):
    
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Case-insensitive duplicate check
        cursor.execute("""
            SELECT product_id
            FROM products
            WHERE LOWER(product_name) = LOWER(?)
        """, (product_name.strip(),))

        existing = cursor.fetchone()

        if existing:
            return None

        cursor.execute("""
            INSERT INTO products
            (product_name, price)
            VALUES (?, ?)
        """, (
            product_name.strip(),
            price
        ))

        connection.commit()

        return cursor.lastrowid

    except sqlite3.Error:
        connection.rollback()
        return None

    finally:
        connection.close()

# ============================================================
# SEARCH PRODUCT
# ============================================================

def search_product(product_id=None, product_name=None):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Search by Product ID
        if product_id is not None:

            cursor.execute("""
                SELECT
                    product_id,
                    product_name,
                    price
                FROM products
                WHERE product_id = ?
            """, (int(product_id),))

        # Search by Product Name
        elif product_name and product_name.strip():

            cursor.execute("""
                SELECT
                    product_id,
                    product_name,
                    price
                FROM products
                WHERE LOWER(product_name) = LOWER(?)
            """, (product_name.strip(),))

        else:
            return []

        return cursor.fetchall()

    except sqlite3.Error:
        return []

    finally:
        connection.close()
# ============================================================
# Show All Products
# ============================================================

def show_products():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT product_id, product_name, price
            FROM products
            ORDER BY product_id
        """)

        products = cursor.fetchall()

        return products

    finally:

        connection.close()


# ============================================================
# Update Product
# ============================================================

def update_product(product_id, product_name, price):

    if price < 0:

        print("Product price cannot be negative.")

        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE products
            SET product_name = ?,
                price = ?
            WHERE product_id = ?
        """, (
            product_name,
            price,
            product_id
        ))

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Product update failed: {e}")

        return False

    finally:

        connection.close()


# ============================================================
# Delete Product
# ============================================================

def delete_product(product_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = ?
        """, (product_id,))

        if cursor.rowcount == 0:

            connection.rollback()

            return False

        connection.commit()

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Product deletion failed: {e}")

        return False

    finally:

        connection.close()