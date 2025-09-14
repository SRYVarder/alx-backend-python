import sqlite3
import functools

def log_queries(func):
    """
    A decorator that logs the SQL query passed to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # The query is expected to be the first positional argument
        query = args[0] if args else kwargs.get('query')
        if query:
            print(f"Executing query: {query}")
        else:
            print("Executing a database operation with an unspecified query.")

        return func(*args, **kwargs)
    return wrapper

# The rest of the provided code
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
