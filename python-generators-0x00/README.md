
# Python Generator - Streaming SQL Rows

This project demonstrates how to use **generators** in Python to stream data from a MySQL database **row by row**, efficiently and with low memory usage.

## 🧩 Features

- Connects to MySQL
- Creates `ALX_prodev` database and `user_data` table
- Populates data from a `user_data.csv` file
- Streams rows using a Python generator function

## 📁 Files

- `seed.py`: Python script with all database logic
- `0-main.py`: Runner file (you write this, or use the provided one)
- `user_data.csv`: CSV containing sample data
- `README.md`: You're reading it!

## 🛠️ Setup

1. Ensure MySQL is running and accessible on `localhost`
2. Create or use a MySQL user (e.g., `root`)
3. Clone this repo or copy the files into your project

### 🔧 Edit `seed.py`

Replace the placeholder password:

```python
password='your_mysql_password'
