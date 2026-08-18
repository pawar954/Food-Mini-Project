# 4.1 create_order.py
import sqlite3

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
# ============================================================
# Update order


def update_order(order_id, order_status, total_amount):

    if total_amount < 0:
        print("Total amount cannot be negative.")
        return False

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE orders
            SET order_status = ?,
                total_amount = ?
            WHERE order_id = ?
        """, (
            order_status,
            total_amount,
            order_id
        ))

        connection.commit()
        if cursor.rowcount == 0:
            print("Order does not exist.")
            return False

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(f"Order update failed: {e}")

        return False

    finally:
        connection.close()