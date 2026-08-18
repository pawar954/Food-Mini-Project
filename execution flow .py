# 1. Customer : 
# 	i. Add_customer : into customer table.
# 2. Product :
# 	i. Add product into product table.
# 3. inventory :
# 	i. Add_inventory :add inventory into inventory table.
# 	ii. update inventory  : updates the inventory when order is successful and it reduces the quantity by minus of order quantity.
# 	iii. delete  : delete the inventory if admin dont whant that product in menu.
# 4. order :
# 	i. add_order: into order_table.
# 				101 p1	pending 0
	
# 	ii. update_order: update status,total amount when quantity is in inventory and 
# 				calculate price then status and price should be change.
	
# 5. order_items :
# 	i. add_order_items: into create_order_item table.
# 6.payments:
# 	i. add_paymnets: into create_payments.
	
        
        #################################
              
#                  ADMIN
#                    │
#         ┌──────────┴──────────┐
#         ↓                     ↓
#      Product              Inventory
#         │                     │
#         └──────────┬──────────┘
#                    ↓
#                 CUSTOMER
#                    ↓
#              Create Order
#                    ↓
#              Order = PENDING
#                    ↓
#             Add Order Items
#                    ↓
#           Check Product Stock
#               ↙         ↘
#           Available    Not Available
#              ↓              ↓
#        Reduce Stock     Reject Order
#              ↓
#        Calculate Total
#              ↓
#            Payment
#              ↓
#        ┌─────┴─────┐
#        ↓           ↓
#     SUCCESS      FAILED
#        ↓           ↓
#    Confirm      Payment
#     Order       Failed
#        ↓
#     Process
#        ↓
#    Complete
   
   
   
#    ###############################################################################
   

###########################################################################################


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
        
################################################################################################

import sqlite3

from database import get_connection

def add_order_item(order_id, product_id, quantity):
    '''
    This function is actually doing two database operations:
    add_order_item()
       ├── INSERT order_items│
       └── UPDATE inventory
       '''

    # Quantity validation
    if quantity <= 0:
        print("Order quantity must be greater than zero.")
        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -----------------------------------------
        # Get product price
        # -----------------------------------------

        cursor.execute("""
            SELECT price
            FROM products
            WHERE product_id = ?
        """, (product_id,)) # the database may return one or more rows.

        product = cursor.fetchone() # "Give me the next single row from the result."

        if product is None:
            print("Product does not exist.")
            return False

        unit_price = product[0]

        # -----------------------------------------
        # Check inventory
        # -----------------------------------------

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

        # -----------------------------------------
        # Check sufficient inventory
        # -----------------------------------------

        if available_quantity < quantity:
            print(
                f"Insufficient inventory. "
                f"Available={available_quantity}, "
                f"Requested={quantity}"
            )
            return False

        # -----------------------------------------
        # Insert order item
        # -----------------------------------------

        cursor.execute("""
            INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            product_id,
            quantity,
            unit_price
        ))

        # -----------------------------------------
        # Reduce inventory
        # -----------------------------------------

        new_quantity = available_quantity - quantity

        cursor.execute("""
            UPDATE inventory
            SET quantity = ?
            WHERE product_id = ?
        """, (
            new_quantity,
            product_id
        ))

        connection.commit()

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Order item creation failed: {e}")

        return False

    finally:

        connection.close()
        
        
        
        
        
        
        
        
        
        ###############################################################################

#                               ADMIN
#                                 │
#                   ┌─────────────┴─────────────┐
#                   ↓                           ↓
#            PRODUCT MANAGEMENT           INVENTORY MANAGEMENT
#                   │                           │
#                   ↓                           ↓
#              add_product()              add_inventory_by_name()
#                   │                           │
#                   ↓                           ↓
#           PRODUCTS TABLE              get_product_id()
#                   │                           │
#                   │                           ↓
#                   │                    product_id found
#                   │                           │
#                   │                           ↓
#                   │                    add_inventory()
#                   │                           │
#                   │                           ↓
#                   │                    INVENTORY TABLE
#                   │
#                   │
#                   ├── update_product()
#                   │
#                   ├── delete_product()
#                   │
#                   └── get_all_products()
#                               │
#                               ↓
#                          CUSTOMER
#                               │
#                               ↓
#                         add_customer()
#                               │
#                               ↓
#                        CUSTOMER TABLE
#                               │
#                               ↓
#                        CREATE ORDER
#                               │
#                               ↓
#                        add_order(101)
#                               │
#                               ↓
#                         ORDERS TABLE
#                               │
#                               ↓
#                         ORDER = PENDING
#                               │
#                               ↓
#                     CUSTOMER SELECTS PRODUCT
#                               │
#                     ┌─────────┴──────────┐
#                     ↓                    ↓
#               Product by Name      Product ID from UI
#                     │                    │
#                     ↓                    │
#        add_order_item_by_name()         │
#                     │                    │
#                     ↓                    │
#              get_product_id()            │
#                     │                    │
#                     ↓                    │
#               product_id = 1             │
#                     │                    │
#                     └─────────┬──────────┘
#                               ↓
#                        add_order_item()
#                               │
#                               ↓
#                      Check Product Exists
#                               │
#                          ┌────┴────┐
#                          ↓         ↓
#                        YES         NO
#                          │         │
#                          ↓         ↓
#                     Get Price    Reject
#                          │
#                          ↓
#                    Check Inventory
#                          │
#                     ┌────┴─────┐
#                     ↓          ↓
#                 AVAILABLE   NOT AVAILABLE
#                     │             │
#                     ↓             ↓
#               Insert Item     Reject Item
#                     │
#                     ↓
#               Reduce Stock
#                     │
#                     ↓
#                  COMMIT
#                     │
#                     ↓
#               Add Next Item
#                     │
#                     ↓
#              All Items Added?
#                     │
#                     ↓
#              Calculate Subtotal
#                     │
#                     ↓
#         Calculate Discount / Tax /
#              Shipping / Total
#                     │
#                     ↓
#                   PAYMENT
#                 /          \
#                /            \
#           SUCCESS            FAILED
#              │                 │
#              ↓                 ↓
#        update_order()    update_order()
#              │                 │
#              ↓                 ↓
#          CONFIRMED       PAYMENT_FAILED
#              │
#              ↓
#          PROCESSING
#              │
#              ↓
#          COMPLETED

# ###############################################################################

# customers
#    customer_id PK

# products
#    product_id PK

# inventory
#    inventory_id PK
#    product_id FK → products

# orders
#    order_id PK
#    customer_id FK → customers

# order_items
#    order_item_id PK
#    order_id FK → orders
#    product_id FK → products

# payments
#    payment_id PK
#    order_id FK → orders
   
   
   
################################################################################################
# Most important functions included

# Product

# add_product()
# get_product_id()
# get_product()
# get_all_products()
# update_product()
# delete_product()

# Inventory

# add_inventory()
# add_inventory_by_name()
# check_inventory()
# update_inventory()
# update_inventory_by_name()
# increase_stock()
# decrease_stock()

# Customer

# add_customer()
# get_customer()
# update_customer()

# Order

# add_order()
# get_order()
# get_customer_orders()
# update_order()

# Order Items

# add_order_item()
# add_order_item_by_name()
# get_order_items()
# calculate_order_total()

# Payment

# create_payment()
# get_payment()\



# ################################################################################

import sqlite3

from database import get_connection

def add_order_item(order_id, product_id, quantity):
    '''
    This function is actually doing two database operations:
    add_order_item()
       ├── INSERT order_items│
       └── UPDATE inventory
       '''

    # Quantity validation
    if quantity <= 0:
        print("Order quantity must be greater than zero.")
        return False

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # -----------------------------------------
        # Get product price
        # -----------------------------------------

        cursor.execute("""
            SELECT price
            FROM products
            WHERE product_id = ?
        """, (product_id,)) # the database may return one or more rows.

        product = cursor.fetchone() # "Give me the next single row from the result."

        if product is None:
            print("Product does not exist.")
            return False

        unit_price = product[0]

        # -----------------------------------------
        # Check inventory
        # -----------------------------------------

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

        # -----------------------------------------
        # Check sufficient inventory
        # -----------------------------------------

        if available_quantity < quantity:
            print(
                f"Insufficient inventory. "
                f"Available={available_quantity}, "
                f"Requested={quantity}"
            )
            return False

        # -----------------------------------------
        # Insert order item
        # -----------------------------------------

        cursor.execute("""
            INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            product_id,
            quantity,
            unit_price
        ))

        # -----------------------------------------
        # Reduce inventory
        # -----------------------------------------

        new_quantity = available_quantity - quantity

        cursor.execute("""
            UPDATE inventory
            SET quantity = ?
            WHERE product_id = ?
        """, (
            new_quantity,
            product_id
        ))

        connection.commit()

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Order item creation failed: {e}")

        return False

    finally:

        connection.close()

