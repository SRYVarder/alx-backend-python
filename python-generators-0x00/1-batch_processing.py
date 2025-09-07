
#!/usr/bin/python3
import seed


def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from user_data in batches of batch_size.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    offset = 0
    while True:
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Process users in batches and print only those older than 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
