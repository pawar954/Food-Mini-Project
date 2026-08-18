import sqlite3

from database import get_connection
from create_product import get_product_id


# ============================================================
# ADD ORDER ITEM
# ============================================================

def add_order_item(order_id, product_id, quantity):

    # --------------------------------------------------------
    # 1. Validate quantity
    # --------------------------------------------------------

    if quantity <= 0:

        print("Order quantity must be greater than zero.")

        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # 2. Get Product Price
        # ----------------------------------------------------
        cursor.execute("""
            SELECT price

            FROM products

            WHERE product_id = ?
        """, (product_id,))

        product = cursor.fetchone()

        if product is None:

            print("Product does not exist.")

            return False

        unit_price = product[0]

        # ----------------------------------------------------
        # 3. Check Inventory
        # ----------------------------------------------------

        cursor.execute("""
            SELECT quantity

            FROM inventory

            WHERE product_id = ?
        """, (product_id,))

        inventory = cursor.fetchone()

        if inventory is None:

            print("Inventory record does not exist.")

            return False

        available_quantity = inventory[0]

        # ----------------------------------------------------
        # 4. Check Sufficient Stock
        # ----------------------------------------------------

        if available_quantity < quantity:

            print(
                f"Insufficient inventory. "
                f"Available={available_quantity}, "
                f"Requested={quantity}"
            )

            return False

        # ----------------------------------------------------
        # 5. Insert Order Item
        # ----------------------------------------------------

        cursor.execute("""
            INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )

            VALUES
                (?, ?, ?, ?)
        """, (
            order_id,
            product_id,
            quantity,
            unit_price
        ))

        # ----------------------------------------------------
        # 6. Reduce Inventory
        # ----------------------------------------------------

        cursor.execute("""
            UPDATE inventory

            SET quantity = quantity - ?

            WHERE product_id = ?
        """, (
            quantity,
            product_id
        ))

        # ----------------------------------------------------
        # 7. Commit Both Operations
        # ----------------------------------------------------

        connection.commit()

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(
            f"Order item creation failed: {e}"
        )

        return False

    finally:

        connection.close()


# # ============================================================
# # ADD ORDER ITEM BY PRODUCT NAME
# # ============================================================

# def add_order_item_by_name(
#     order_id,
#     product_name,
#     quantity
# ):

#     # --------------------------------------------------------
#     # Get Product ID
#     # --------------------------------------------------------

#     product_id = get_product_id(
#         product_name
#     )

#     if product_id is None:

#         return False

#     # --------------------------------------------------------
#     # Call Actual Order Item Function
#     # --------------------------------------------------------

#     return add_order_item(
#         order_id,
#         product_id,
#         quantity
#     )

