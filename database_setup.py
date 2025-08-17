import sqlite3

def create_connection():
    return sqlite3.connect("university.db")

def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            prn INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            department TEXT NOT NULL,
            gender TEXT NOT NULL,
            starting_year INTERGER NOT NULL,
            duration INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            name TEXT PRIMARY KEY,
            experience INTEGER NOT NULL,
            education TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def add_record(table, values):
    conn = create_connection()
    cursor = conn.cursor()
    if table == "students":
        cursor.execute("""
            INSERT INTO students (prn, name, age, address, phone, email, department, gender, starting_year, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, values)
    elif table == "faculty":
        cursor.execute("""
            INSERT INTO faculty (name, experience, education, teaches)
            VALUES (?, ?, ?, ?)
        """, values)
    conn.commit()
    conn.close()

def fetch_records(table):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()
    conn.close()
    return records

def check_duplicate_prn(prn):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE prn = ?", (prn,))
    record = cursor.fetchone()
    conn.close()
    return record is not None

def check_duplicate_faculty_name(faculty_name): 
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty WHERE name = ?", (faculty_name,))
    record = cursor.fetchone()
    conn.close()
    return record is not None


def has_data(table):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0