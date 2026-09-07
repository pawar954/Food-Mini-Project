# step 1 . Create database  database.py

import sqlite3
DATABASE_NAME = "food_order.db"

def get_connection():
    '''
    Whenever the application needs to communicate with the database, call this function to get a database connection.
    '''
    connection = sqlite3.connect(DATABASE_NAME)

    return connection # opens a connection to our SQLite database.
	
#done


#Step 2 — Test the connection main.py    

from database import get_connection #

def main():
    connection = get_connection() # This represents the connection/session between your Python application and SQLite.
    print("Database connection successful.")
    connection.close()

if __name__ == "__main__":
    main()
#done



# ┌──────────────────────────────┐
# │          CUSTOMERS           │
# ├──────────────────────────────┤
# │ PK  customer_id              │
# │     name                     │
# │ UQ  phone                    │
# │     email                    │
# └──────────────┬───────────────┘
#                │
#                │ 1
#                │
#                │ N
#                ▼
# ┌──────────────────────────────┐
# │           ORDERS             │
# ├──────────────────────────────┤
# │ PK  order_id                 │
# │ FK  customer_id              │
# │     order_date               │
# │     status                   │
# │     total_amount             │
# └──────────────┬───────────────┘
#                │
#                │ 1
#                │
#                │ N
#                ▼
# ┌──────────────────────────────┐
# │        ORDER_ITEMS           │
# ├──────────────────────────────┤
# │ PK  order_item_id            │
# │ FK  order_id                 │
# │ FK  product_id               │
# │     quantity                 │
# │     unit_price               │
# └──────────────┬───────────────┘
#                │
#                │ N
#                │
#                │ 1
#                ▼
# ┌──────────────────────────────┐
# │          PRODUCTS            │
# ├──────────────────────────────┤
# │ PK  product_id               │
# │ UQ  product_name             │
# │     price                    │
# └──────────────┬───────────────┘
#                │
#                │ 1
#                │
#                │ 1
#                ▼
# ┌──────────────────────────────┐
# │          INVENTORY           │
# ├──────────────────────────────┤
# │ PK  product_id               │
# │     quantity                 │
# └──────────────────────────────┘


# ┌──────────────────────────────┐
# │           ORDERS             │
# │          order_id            │
# └──────────────┬───────────────┘
#                │
#                │ 1
#                │
#                │ N
#                ▼
# ┌──────────────────────────────┐
# │          PAYMENTS            │
# ├──────────────────────────────┤
# │ PK  payment_id               │
# │ FK  order_id                 │
# │     payment_date             │
# │     amount                   │
# │     payment_status           │
# └──────────────────────────────┘





#Step 3 create_table.py

from database import get_connection

def create_tables():

    connection = get_connection()#This represents the connection/session between your Python application and SQLite.
    
    cursor = connection.cursor() # The cursor is an object that allows Python to execute SQL statements 
                                 # against that database connection and, 
                                 # for queries, retrieve results.
    '''
    "Cursor, execute this SQL statement against the database."
    '''
    
    # -------------------------
    # Customers
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            email TEXT
        )
    """)

    # -------------------------
    # Products
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL CHECK (price >= 0)
        )
    """)

    # -------------------------
    # Inventory
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            product_id INTEGER PRIMARY KEY,
            quantity INTEGER NOT NULL CHECK (quantity >= 0),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    # -------------------------
    # Orders
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            total_amount REAL NOT NULL DEFAULT 0,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """)

    # -------------------------
    # Order Items
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price REAL NOT NULL CHECK (unit_price >= 0),

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        )
    """)

    # -------------------------
    # Payments
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            payment_date TEXT NOT NULL,
            amount REAL NOT NULL CHECK (amount >= 0),
            payment_status TEXT NOT NULL,

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id)
        )
    """)

    connection.commit()
    connection.close()

    print("All tables created successfully.")


if __name__ == "__main__":
    create_tables()
	
#done





# 4.1 create_customer.py

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
#done
	
#test
#4.1.1 test_code.py 

import sqlite3
from create_customer import add_customers


def test_add_customers():

    customers = [
        ("Neha", "9876543211", "neha@gmail.com"),
        ("Ravi", "9876543212", "ravi@gmail.com"),
        ("Sneha", "9876543213", "sneha@gmail.com"),
        ("Priya", "9876543214", "priya@gmail.com")
    ]

    for customer in customers:

        customer_id = add_customer(
            customer[0],
            customer[1],
            customer[2]
        )

        print(
            f"Customer created: "
            f"ID={customer_id}, "
            f"Name={customer[0]}"
        )

if __name__ == "__main__":
    test_add_customers()
    
 #done
 
#4.2. create_product.py
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
        
#4.2.2 test_code.py
import sqlite3
from create_product import add_products


def test_add_products():

    products = [
        ("Margherita Pizza",299 ),
        ("Veg Burger",149),
        ("French Fries",99),
        ("Paneer Tikka",249 ),
        ("Masala Dosa",129),
        ("White Sauce Pasta", 229),
        ("Chocolate Brownie",129 ),
        ("Cold Coffee",119 ),
        ("Pav Bhaji",149 ),
        ("Cheese Garlic Bread",159 )
    ]

    for product in products:

        product_id = add_products(
            product[0],
            product[1]
        )

        print(
            f"Products created: "
            f"ID={product_id}, "
            f"Name={product[0]}"
        )

if __name__ == "__main__":
    test_add_products()
#Done



#4.3 create_inventory.py
import sqlite3
from database import get_connection
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
        
 #done

#4.3.1 test_add_inventory
from create_inventory import add_inventory


def test_add_inventory():

    inventorys = [
        (1,20 ),
        (2,49),
        (3,9),
        (4,24 ),
        (5,29),
        (6, 22),
        (7,12 ),
        (8,19 ),
        (9,149 ),
        (10,59 )
    ]

    for inventory in inventorys:

        inventory_id = add_inventory(
            inventory[0],
            inventory[1]
        )

        print(
            f"Inventory created: "
            f"Product ID={inventory_id}, "
            f"Quantity={inventory[1]}"
        )

if __name__ == "__main__":
    test_add_inventory()
   
#4.4 create_order.py
from database import get_connection

def add_order(customer_id,order_date,status,total_amount):
    connection=get_connection()
    
    try:
        cursor=connection.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date,status,total_amount)
            VALUES (?, ?,?,?)
        """, (customer_id, order_date,status,total_amount))
        connection.commit()
        
        order_id=cursor.lastrowid
        return order_id
    except Exception as e:

        connection.rollback()

        print(f"Order creation failed: {e}")

        return None

    finally:

        connection.close()
        
#done

#4.4.1 test
from create_order import add_order


def test_add_order():

    orders = [
        (1, "2026-08-16", "Pending", 548),
        (2, "2026-08-16", "Confirmed", 399),
        (3, "2026-08-16", "Preparing", 699),
        (4, "2026-08-16", "Delivered", 249),
        (5, "2026-08-16", "Pending", 459),
        (6, "2026-08-16", "Confirmed", 799),
        (7, "2026-08-16", "Preparing", 329),
        (8, "2026-08-16", "Delivered", 599),
        (9, "2026-08-16", "Pending", 449),
        (10, "2026-08-16", "Confirmed", 899)
    ]

    for order in orders:

        order_id = add_order(
            order[0],
            order[1],
            order[2],
            order[3]
        )

        print(
            f"Order created: "
            f"Order ID={order_id}, "
            f"Customer ID={order[0]}, "
            f"Status={order[2]}, "
            f"Total={order[3]}"
        )

if __name__ == "__main__":
    test_add_order()
#done 
    
#4.5 create_order_item.py
from database import get_connection


def add_order_items(order_id, product_id, quantity, unit_price):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """, (order_id, product_id, quantity, unit_price))

        connection.commit()

        order_item_id = cursor.lastrowid

        return order_item_id

    except Exception as e:

        connection.rollback()

        print(f"Order item creation failed: {e}")

        return None

    finally:

        connection.close()
      ##done#  
        
##4.5.1 test
        
from create_order_item import add_order_items


def test_add_order_items():

    order_items = [
        (1, 1, 2, 299),
        (1, 3, 1, 99),
        (2, 2, 2, 149),
        (2, 5, 1, 129),
        (3, 4, 2, 249),
        (3, 6, 1, 229),
        (4, 7, 3, 129),
        (5, 8, 2, 119),
        (6, 9, 1, 149),
        (7, 10, 2, 159)
    ]

    for item in order_items:

        order_item_id = add_order_items(
            item[0],
            item[1],
            item[2],
            item[3]
        )

        print(
            f"Order item created: "
            f"ID={order_item_id}, "
            f"Order ID={item[0]}, "
            f"Product ID={item[1]}, "
            f"Quantity={item[2]}, "
            f"Unit Price={item[3]}"
        )


if __name__ == "__main__":
    test_add_order_items()

        
      ##done##    



#4.6 create_payments.py
from database import get_connection


def add_payment(order_id, payment_date, amount, payment_status):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO payments
            (order_id, payment_date, amount, payment_status)
            VALUES (?, ?, ?, ?)
        """, (order_id, payment_date, amount, payment_status))

        connection.commit()

        payment_id = cursor.lastrowid

        return payment_id

    except Exception as e:

        connection.rollback()

        print(f"Payment creation failed: {e}")

        return None

    finally:

        connection.close()
        
        ###done#
        
        
 
#4.6.1  test payments
from create_payments import add_payment


def test_add_payments():

    payments = [
        (1, "2026-08-16", 548, "Paid"),
        (2, "2026-08-16", 399, "Paid"),
        (3, "2026-08-16", 699, "Pending"),
        (4, "2026-08-16", 249, "Paid"),
        (5, "2026-08-16", 459, "Pending"),
        (6, "2026-08-16", 799, "Paid"),
        (7, "2026-08-16", 329, "Failed"),
        (8, "2026-08-16", 599, "Paid"),
        (9, "2026-08-16", 449, "Pending"),
        (10, "2026-08-16", 899, "Paid")
    ]

    for payment in payments:

        payment_id = add_payment(
            payment[0],
            payment[1],
            payment[2],
            payment[3]
        )

        print(
            f"Payment created: "
            f"Payment ID={payment_id}, "
            f"Order ID={payment[0]}, "
            f"Amount={payment[2]}, "
            f"Amount={payment[2]}, "
            f"Status={payment[3]}"
        )


if __name__ == "__main__":
    test_add_payments()

##done##


#customer: create :- done , insert,tested:- done
#product: create :- done , insert,tested:- done
#inventory: create :- done , insert,tested:- done
#orders: create :- done , insert,tested:- done
#order_items: create :- done , insert,tested:- done
#payments: create :- done , insert,tested:- done




