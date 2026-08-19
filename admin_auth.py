import hashlib
import sqlite3

from database import get_connection


# ============================================================
# HASH PASSWORD
# ============================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# CREATE ADMIN
# ============================================================

def create_admin(
    username,
    password,
    full_name
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        password_hash = hash_password(password)

        cursor.execute("""
            INSERT INTO admin_users
            (
                username,
                password_hash,
                full_name,
                is_active
            )
            VALUES (?, ?, ?, 1)
        """, (
            username,
            password_hash,
            full_name
        ))

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:

        connection.rollback()

        return None

    finally:

        connection.close()


# ============================================================
# VALIDATE ADMIN
# ============================================================

def validate_admin(
    username,
    password
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        password_hash = hash_password(password)

        cursor.execute("""
            SELECT
                admin_id,
                username,
                full_name
            FROM admin_users
            WHERE username = ?
            AND password_hash = ?
            AND is_active = 1
        """, (
            username,
            password_hash
        ))

        return cursor.fetchone()

    finally:

        connection.close()



# ============================================================
# SHOW ADMINS
# ============================================================

def show_admins():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                admin_id,
                username,
                full_name,
                CASE
                    WHEN is_active = 1 THEN 'Active'
                    ELSE 'Inactive'
                END AS status
            FROM admin_users
            ORDER BY admin_id
        """)

        return cursor.fetchall()

    finally:

        connection.close()