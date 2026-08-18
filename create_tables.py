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

####done###


