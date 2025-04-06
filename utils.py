import os
import re
import pymysql
from pdfminer.high_level import extract_text
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
        return ""

def connect_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

def store_to_db(name, email, phone, file_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            file_name VARCHAR(255)
        )
    """)
    insert_query = """
        INSERT INTO resumes (name, email, phone, file_name)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, email, phone, file_name))
    conn.commit()
    cursor.close()
    conn.close()
