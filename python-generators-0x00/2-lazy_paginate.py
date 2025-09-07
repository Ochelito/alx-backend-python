#!/usr/bin/env python3
"""
Lazy loading pagination using Python generators
"""
import seed


def paginate_users(page_size, offset):

    #Fetch a single page of users from the DB.

    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Lazily fetches user_data in pages of `page_size`.
    Yields one page (list of users) at a time.
    Uses only one loop.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # stop if no more data
            break
        yield page
        offset += page_size