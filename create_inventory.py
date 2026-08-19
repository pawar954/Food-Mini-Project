# inventory :
import sqlite3

from database import get_connection


# ============================================================
# Add inventory
# ============================================================

def add_inventory(product_id, quantity):

    if quantity < 0:
        print("Inventory quantity cannot be negative.")
        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO inventory (product_id, quantity)
            VALUES (?, ?)
        """, (product_id, quantity))

        connection.commit()

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Inventory creation failed: {e}")

        return False

    finally:

        connection.close()


# ============================================================
# Check inventory
# ============================================================

def check_inventory(product_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT quantity
            FROM inventory
            WHERE product_id = ?
        """, (product_id,))

        result = cursor.fetchone()

        if result is None:
            return 0

        return result[0]

    finally:

        connection.close()


# ============================================================
# Update inventory
# ============================================================

def update_inventory(product_id, quantity):

    if quantity < 0:
        print("Inventory quantity cannot be negative.")
        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE inventory
            SET quantity = ?
            WHERE product_id = ?
        """, (quantity, product_id))

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Inventory update failed: {e}")

        return False

    finally:

        connection.close()

# ============================================================
# Delete inventory
# ============================================================

def delete_inventory(product_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM inventory
            WHERE product_id = ?
        """, (product_id,))

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.Error as e:

        connection.rollback()

        print(f"Inventory deletion failed: {e}")

        return False

    finally:

        connection.close()
# ============================================================
# Show inventory
# ============================================================

def show_inventory():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                i.quantity
            FROM products p
            JOIN inventory i
                ON p.product_id = i.product_id
            ORDER BY p.product_id
        """)

        inventory = cursor.fetchall()

        return inventory

    finally:

        connection.close()



# ============================================================
# SEARCH INVENTORY
# ============================================================

def search_inventory(product_id=None, product_name=None):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # Search by Product ID
        # ----------------------------------------------------

        if product_id is not None:

            cursor.execute("""
                SELECT
                    i.product_id,
                    p.product_name,
                    i.quantity
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
                WHERE i.product_id = ?
            """, (int(product_id),))

        # ----------------------------------------------------
        # Search by Product Name
        # ----------------------------------------------------

        elif product_name and product_name.strip():

            cursor.execute("""
                SELECT
                    i.product_id,
                    p.product_name,
                    i.quantity
                FROM inventory i
                JOIN products p
                    ON i.product_id = p.product_id
                WHERE LOWER(p.product_name) = LOWER(?)
            """, (product_name.strip(),))

        else:

            return []

        return cursor.fetchall()

    except sqlite3.Error:

        return []

    finally:

        connection.close()