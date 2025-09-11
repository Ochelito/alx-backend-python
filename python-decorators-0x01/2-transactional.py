import sqlite3 
import functools

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

# ---- Transactional decorator ----
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if no exceptions
            return result
        except Exception as e:
            conn.rollback()  # Rollback on exception
            print(f"Transaction failed: {e}")
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')