import time
import sqlite3 
import functools

# ---- global cache dictionary ----
query_cache = {}

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

def cache_query(func):
    """
    Caches query results based on the query string.
    Uses a global dictionary query_cache to store results.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
         # Extract query string (assumes it’s passed as a kwarg OR second positional arg)
        query = kwargs.get('query')
        if query is None and len(args) > 1:
            query = args[1]

        # Check if query result is already cached
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        
        # Otherwise, execute the function and cache the result
        print(f"Cache miss for query: {query}. Executing and caching result.") 
        result = func(*args, **kwargs)
        query_cache[query] = result #cache the result
        return result
    return wrapper

# ---- Function using cache + connection handling ----
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call->cache miss (runs query) will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call->cache hit (returns cached result, no DB call) will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users)
print(users_again)