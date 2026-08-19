# 4.3 create_payment.py

import sqlite3
from datetime import datetime

from database import get_connection


# ============================================================
# ADD PAYMENT
# ============================================================

def add_payment(order_id, payment_date, amount, payment_status):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        # ----------------------------------------------------
        # 1. Check Order
        # ----------------------------------------------------

        cursor.execute("""
            SELECT total_amount
            FROM orders
            WHERE order_id = ?
        """, (order_id,))

        order = cursor.fetchone()

        if order is None:

            print("Order does not exist.")

            return None

        total_amount = order[0]

        # ----------------------------------------------------
        # 2. Validate Payment Amount
        # ----------------------------------------------------

        if amount <= 0:

            print("Payment amount must be greater than zero.")

            return None

        if amount != total_amount:

            print(
                f"Payment amount must be {total_amount}."
            )

            return None

        # ----------------------------------------------------
        # 3. Check Existing Successful Payment
        # ----------------------------------------------------

        cursor.execute("""
            SELECT payment_id
            FROM payments
            WHERE order_id = ?
            AND payment_status = ?
        """, (
            order_id,
            "SUCCESS"
        ))

        existing_payment = cursor.fetchone()

        if existing_payment is not None:

            print("Payment already completed for this order.")

            return None

        # ----------------------------------------------------
        # 4. Insert Payment
        # ----------------------------------------------------

        cursor.execute("""
            INSERT INTO payments
            (
                order_id,
                payment_date,
                amount,
                payment_status
            )
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            payment_date,
            amount,
            payment_status
        ))

        payment_id = cursor.lastrowid

        # ----------------------------------------------------
        # 5. If Payment Successful
        # ----------------------------------------------------

        if payment_status == "SUCCESS":

            updated_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute("""
                UPDATE orders

                SET status = ?,
                    updated_at = ?

                WHERE order_id = ?
            """, (
                "CONFIRMED",
                updated_time,
                order_id
            ))

        # ----------------------------------------------------
        # 6. Commit
        # ----------------------------------------------------

        connection.commit()

        return payment_id

    except sqlite3.IntegrityError as e:

        connection.rollback()

        print(
            f"Payment creation failed: {e}"
        )

        return None

    except Exception as e:

        connection.rollback()

        print(
            f"Payment creation failed: {e}"
        )

        return None

    finally:

        connection.close()


# ============================================================
# PAYMENT SUCCESS HELPER
# ============================================================

def make_payment(order_id, amount):

    payment_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return add_payment(
        order_id,
        payment_date,
        amount,
        "SUCCESS"
    )