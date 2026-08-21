import sqlite3

def create_connection():
    conn = sqlite3.connect("Student.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Studentdb (
            NID INTEGER PRIMARY KEY AUTOINCREMENT,
            F_name TEXT(50) NOT NULL,
            L_name TEXT(50) NOT NULL,
            B_date DATE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Enrollment (
            Student_code INTEGER PRIMARY KEY AUTOINCREMENT,
            Date_of_enrolment DATE NOT NULL,
            Course_name TEXT(100) NOT NULL,
            CC_no INTEGER NOT NULL,
            FOREIGN KEY (CC_no) REFERENCES Lecture(CC_no)
        );

        CREATE TABLE IF NOT EXISTS Lecture (
            CC_no INTEGER PRIMARY KEY,
            Subject TEXT(100) NOT NULL,
            Time TEXT(20) NOT NULL,
            Date DATE NOT NULL,
            Lecture_name TEXT(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Lecturerdb (
            Lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,
            L_lastname TEXT(50) NOT NULL,
            L_firstname TEXT(50) NOT NULL,
            L_email TEXT(100) NOT NULL UNIQUE,
            L_address TEXT(200) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Subjectsdb (
            Subject_code INTEGER PRIMARY KEY,
            Subject_unit INTEGER NOT NULL,
            Subject_udsc TEXT(200) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Enrolls (
            NID INTEGER NOT NULL,
            Student_code INTEGER NOT NULL,
            CC_no INTEGER NOT NULL,
            PRIMARY KEY (NID, Student_code, CC_no),
            FOREIGN KEY (NID) REFERENCES Student(NID),
            FOREIGN KEY (Student_code) REFERENCES Enrollment(Student_code),
            FOREIGN KEY (CC_no) REFERENCES Lecture(CC_no)
        );

        CREATE TABLE IF NOT EXISTS Lectures (
            Lecture_id INTEGER NOT NULL,
            CC_no INTEGER NOT NULL,
            Subject_code INTEGER NOT NULL,
            PRIMARY KEY (Lecture_id, CC_no, Subject_code),
            FOREIGN KEY (Lecture_id) REFERENCES Lecturer(Lecture_id),
            FOREIGN KEY (CC_no) REFERENCES Lecture(CC_no),
            FOREIGN KEY (Subject_code) REFERENCES Subjects(Subject_code)
        );
    ''')
    conn.commit()
    conn.close()
