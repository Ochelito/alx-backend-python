import mysql.connector
import csv
import uuid
import os

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "Linkwithaugustine@gmail.com"),
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create database if it does not exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev ensured.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

# Connect to ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Linkwithaugustine@gmail.com", 
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

# Create user_data table if it does not exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                UNIQUE KEY(email)
            );
        """)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# Insert CSV data into user_data table
def insert_data(connection, file_path):
    try:
        cursor = connection.cursor()
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Generate UUID if missing
                user_id = row.get('user_id') or str(uuid.uuid4())
                # Insert data if not exists
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Exception as err:
        print(f"Error inserting data: {err}")

# Generator to stream rows one by one
def stream_rows(connection, batch_size=10):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        for row in rows:
            yield row
    cursor.close()