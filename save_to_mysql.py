# save_to_mysql.py

import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Step 1: Create connection
def connect_mysql():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Step 2: Initialize DB and Table
def initialize_database():
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS langchain_responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_input TEXT,
            llm_response TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Step 3: Insert data into table
def insert_to_database(user_input, llm_response):
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO langchain_responses (user_input, llm_response) VALUES (%s, %s)",
        (user_input, llm_response)
    )
    conn.commit()
    cursor.close()
    conn.close()
