
#!/usr/bin/python3
import seed


def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    Yields dict objects representing each user.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
