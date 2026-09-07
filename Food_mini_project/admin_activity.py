from datetime import datetime

from database import get_connection


# ============================================================
# LOG ACTIVITY
# ============================================================

def log_activity(
    admin_id,
    action,
    details
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        action_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute("""
            INSERT INTO admin_activity_logs
            (
                admin_id,
                action,
                details,
                action_time
            )
            VALUES (?, ?, ?, ?)
        """, (
            admin_id,
            action,
            details,
            action_time
        ))

        connection.commit()

    finally:

        connection.close()


# ============================================================
# SHOW ACTIVITY
# ============================================================

def show_activity():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                l.log_id,
                a.username,
                l.action,
                l.details,
                l.action_time
            FROM admin_activity_logs l
            JOIN admin_users a
                ON l.admin_id = a.admin_id
            ORDER BY l.log_id DESC
        """)

        return cursor.fetchall()

    finally:

        connection.close()