import sqlite3

from database import get_connection
from create_product import get_product_id



def add_inventory(product_id,quantity):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO inventory (product_id, quantity)
            VALUES (?, ?)
        """, (product_id, quantity))

        connection.commit()
        return product_id

    except Exception as e:

        connection.rollback()

        print(f"Inventory creation failed: {e}")

        return None

    finally:

        connection.close()



# ==========================================================================================

# ADD INVENTORY BY PRODUCT NAME


def add_inventory_by_name(product_name, quantity):

    product_id = get_product_id(product_name)

    if product_id is None:

        return False

    return add_inventory(
        product_id,
        quantity
    )


# ============================================================
# CHECK INVENTORY


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
# UPDATE INVENTORY


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
        """, (
            quantity,
            product_id
        ))

        connection.commit()

        return cursor.rowcount > 0

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Inventory update failed: {e}")

        return False

    finally:

        connection.close()


# ============================================================
# UPDATE INVENTORY BY PRODUCT NAME


def update_inventory_by_name(product_name, quantity):

    product_id = get_product_id(product_name)

    if product_id is None:

        return False

    return update_inventory(
        product_id,
        quantity
    )

