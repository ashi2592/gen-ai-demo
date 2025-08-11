# utils/db_utils.py
import os
import sqlite3

def get_db_connection(db_name: str = "agent_data.db"):
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(os.path.join("data", db_name))
    return conn


def execute_query_without_no_value(query: str, params: tuple = ()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return 

def execute_query_with_fetch_all(query: str, params: tuple = ()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows= cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

def execute_query_with_fetch_one(query: str, params: tuple = ()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row

def execute_query_with_lastrowid(query: str, params: tuple = ()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    last_row_id = cursor.lastrowid
    return last_row_id
