#!/usr/bin/env python3
"""
Generator function to stream rows from user_data table
"""
import os
import mysql.connector


def stream_users():
    """
    Connects to ALX_prodev DB and yields user_data rows one by one
    using a Python generator.
    """
    connection = None
    cursor = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "Linkwithaugustine@gmail.com"),
            database="ALX_prodev"
        )

        # buffered=True prevents "Unread result found" errors
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            yield row

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()