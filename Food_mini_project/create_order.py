# 4.1 create_order.py

import sqlite3
from datetime import datetime

from database import get_connection


# ============================================================
# CREATE ORDER
# ============================================================

def add_order(customer_id, status="PENDING", total_amount=0):

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO orders
            (
                customer_id,
                created_at,
                updated_at,
                status,
                total_amount
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            customer_id,
            current_time,
            current_time,
            status,
            total_amount
        ))

        connection.commit()

        order_id = cursor.lastrowid

        return order_id

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(
            f"Order creation failed: {e}"
        )

        return None

    finally:

        connection.close()


# ============================================================
# UPDATE ORDER
# ============================================================

def update_order(order_id, order_status, total_amount):

    if total_amount < 0:

        print(
            "Total amount cannot be negative."
        )

        return False

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE orders

            SET status = ?,
                total_amount = ?,
                updated_at = ?

            WHERE order_id = ?
        """, (
            order_status,
            total_amount,
            current_time,
            order_id
        ))

        connection.commit()

        if cursor.rowcount == 0:

            print(
                "Order does not exist."
            )

            return False

        return True

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(
            f"Order update failed: {e}"
        )

        return False

    finally:

        connection.close()