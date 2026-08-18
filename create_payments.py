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