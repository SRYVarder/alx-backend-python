import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that handles the database connection for the decorated function.
    It opens a connection, passes it to the function, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Establish the connection
            conn = sqlite3.connect('users.db')
            
            # Pass the connection object as the first argument to the original function
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error occurred: {e}")
            raise # Re-raise the exception to be handled by the caller
        finally:
            # Close the connection, ensuring it happens even if an exception was raised
            if conn:
                conn.close()
    return wrapper

# The rest of the provided code
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
