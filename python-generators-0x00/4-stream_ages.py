#!/usr/bin/env python3
"""
Task 4: Memory-Efficient Aggregation with Generators
Compute average age using a generator without loading all rows into memory.
"""

import seed  # reuse DB connection helper from seed.py


def stream_user_ages():
    """
    Generator that streams user ages one by one from the user_data table.
    Yields:
        int: age of each user
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")

        for row in cursor:  # single loop
            yield int(row["age"])

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def calculate_average_age():
    """
    Uses the age generator to calculate the average age of all users.
    Prints the average age.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # second loop
        total += age
        count += 1

    avg = total / count if count > 0 else 0
    print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    calculate_average_age()