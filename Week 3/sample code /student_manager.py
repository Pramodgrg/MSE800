import sqlite3
from database import create_connection


def add_student(F_name, L_name, B_date):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Studentdb (F_name, L_name, B_date) VALUES (?, ?, ?)", (F_name, L_name, B_date))
        conn.commit()
        print(" User added successfully.")
    except sqlite3.IntegrityError:
        print(" Something went wrong")
    conn.close()

def view_student():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Studentdb")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_subject(Subject_code, Subject_unit, Subject_udsc):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Subjectsdb (Subject_code, Subject_unit, Subject_udsc) VALUES (?, ?, ?)", (Subject_code, Subject_unit, Subject_udsc))
        conn.commit()
        print(" Course added successfully.")
    except sqlite3.IntegrityError:
        print(" Something went wrong")
    conn.close()

def view_subject():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Subjectsdb")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_lecturer(L_firstname, L_lastname, L_email, L_address):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Lecturerdb (L_firstname, L_lastname, L_email, L_address) VALUES (?, ?, ?, ?)", (L_firstname, L_lastname, L_email, L_address))
        conn.commit()
        print(" lecturer added successfully.")
    except sqlite3.IntegrityError:
        print(" Something went wrong")
    conn.close()

def view_lecturer():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Lecturerdb")
    rows = cursor.fetchall()
    conn.close()
    return rows