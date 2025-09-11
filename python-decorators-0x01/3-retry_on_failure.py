import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
       
        conn = sqlite3.connect('users.db')  #open a database connection automatically
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close() #ensure the connection is closed(even on error)
    return wrapper

#### decorator to retry on failure
def retry_on_failure(retries=3, delay=2):
      
    """
    Retries a database operation if it fails due to an exception.
    :param retries: how many times to retry
    :param delay: how many seconds to wait between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs) #try to execute the function
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            raise last_exception  #raise the last exception if all retries fail
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)