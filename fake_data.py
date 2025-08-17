import sqlite3
import random
import faker
from random import choice

# Initialize faker to generate random data
fake = faker.Faker()

# Department list
departments = ["Computer Engineering", "Information Technology", "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering", "Petrochemical Engineering"]

# Connect to SQLite database (or create it)
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Create tables if they don't exist
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
        starting_year INTEGER NOT NULL,
        duration INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        name TEXT PRIMARY KEY,
        experience INTEGER NOT NULL,
        education TEXT NOT NULL,
        teaches TEXT NOT NULL
    )
""")

# Function to generate random student data
def generate_student(existing_prns):
    prn = random.randint(100000000, 999999999)
    # Ensure unique PRN
    while prn in existing_prns:
        prn = random.randint(100000000, 999999999)
    
    existing_prns.add(prn)  # Add the PRN to the set of existing PRNs
    
    name = fake.name()
    age = random.randint(18, 30)
    address = fake.address().replace("\n", " ")
    phone = fake.phone_number()
    email = fake.email()
    department = choice(departments)
    gender = choice(["Male", "Female", "Other"])
    starting_year = random.randint(2010, 2024)
    duration = random.randint(4, 6)
    
    return (prn, name, age, address, phone, email, department, gender, starting_year, duration)

# Function to generate random faculty data
def generate_faculty(existing_faculty_names):
    name = fake.name()
    # Ensure unique faculty name
    while name in existing_faculty_names:
        name = fake.name()

    existing_faculty_names.add(name)  # Add the name to the set of existing faculty names
    
    experience = random.randint(1, 30)
    education = choice(["BSc", "MSc", "PhD"])
    teaches = choice(departments)
    
    return (name, experience, education, teaches)

# Sets to keep track of existing records
existing_prns = set()
existing_faculty_names = set()

# Insert 10,000 unique student records
for _ in range(10000):  # Adjusted to 10,000
    student_data = generate_student(existing_prns)
    cursor.execute("""
        INSERT INTO students (prn, name, age, address, phone, email, department, gender, starting_year, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, student_data)

# Insert 10,000 unique faculty records
for _ in range(5000):  # Adjusted to 10,000
    faculty_data = generate_faculty(existing_faculty_names)
    cursor.execute("""
        INSERT INTO faculty (name, experience, education, department)
        VALUES (?, ?, ?, ?)
    """, faculty_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("10,000 unique student and faculty records inserted successfully.")
