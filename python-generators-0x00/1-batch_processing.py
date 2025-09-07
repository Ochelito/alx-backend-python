#!/usr/bin/env python3
"""
Batch processing with generators for user_data table
"""
import os
import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from user_data in batches of `batch_size`.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "Linkwithaugustine@gmail.com"),
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return  # Explicitly end the generator

def batch_processing(batch_size):
    """
    Process each batch and print users older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
    return  # Explicitly end the generator