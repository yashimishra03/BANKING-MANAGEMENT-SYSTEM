"""
db.py
-----
Handles the MySQL connection for the Banking Management System.

Update the credentials below (or set them as environment variables)
before running the app.
"""

import os
import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "yashi2007"),
    "database": os.getenv("DB_NAME", "banking_system"),
}


def get_connection():
    """Return a fresh MySQL connection. Raises mysql.connector.Error on failure."""
    return mysql.connector.connect(**DB_CONFIG)


def run_query(query, params=None, fetch=False, fetchone=False, commit=False):
    """
    Generic helper to run a query safely.

    fetch      -> returns list of dict rows
    fetchone   -> returns single dict row (or None)
    commit     -> commits (for INSERT/UPDATE/DELETE) and returns lastrowid
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if commit:
            conn.commit()
            return cursor.lastrowid

        if fetchone:
            return cursor.fetchone()

        if fetch:
            return cursor.fetchall()

        return None
    except Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def init_db():
    """Create tables if they do not already exist (run schema.sql)."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        with open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r") as f:
            sql_script = f.read()
        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except:
                    pass
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
