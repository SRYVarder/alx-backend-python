
#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator that yields ages of users one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def compute_average_age():
    """Compute average age using the stream_user_ages generator."""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("No users found.")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    compute_average_age()
