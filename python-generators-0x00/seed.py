
#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid


def connect_db():
    """Connects to the MySQL server (no database specified yet)"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password'  # <-- Replace with your actual password
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_database(connection):
    """Creates ALX_prodev database if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Database creation error: {e}")


def connect_to_prodev():
    """Connects directly to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # <-- Replace with your actual password
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Connection to ALX_prodev failed: {e}")
        return None


def create_table(connection):
    """Creates the user_data table"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            );
        """)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_filename):
    """Inserts user data from a CSV file into the table"""
    try:
        cursor = connection.cursor()
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                cursor.execute("""
                    SELECT * FROM user_data WHERE email = %s
                """, (email,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
        print("CSV data inserted successfully.")
    except Error as e:
        print(f"Data insertion error: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_filename} not found.")


def stream_users(connection):
    """Generator that yields user records one at a time"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except Error as e:
        print(f"Error streaming data: {e}")
