# Week 2 - Activity 3: Data Types with Description

class Student:
    """
    This class represents one student.
    It stores the student's personal information.
    """

    def __init__(self, full_name, age, address, student_id):
        # str: stores text such as the student's full name.
        self.full_name = full_name

        # int: stores the student's age as a whole number.
        self.age = age

        # str: stores text containing the student's address.
        self.address = address

        # str: Student IDs are stored as strings because they may
        # contain leading zeros or letters in some systems.
        self.student_id = student_id

    def display_information(self):
        """Display the student's information."""
        print(f"Student ID: {self.student_id}")
        print(f"Full Name: {self.full_name}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print("-" * 30)


def main():
    # list: stores multiple Student objects.
    # The list can contain 70 students or any unknown number of students.
    students = []

    # int: stores the number of students entered by the user.
    number_of_students = int(input("How many students do you want to enter? "))

    # range() generates numbers from 0 up to the number of students.
    for i in range(number_of_students):
        print(f"\nEnter information for Student {i + 1}")

        # str: stores the student's full name.
        full_name = input("Full Name: ")

        # int: converts the user's input into a whole number.
        age = int(input("Age: "))

        # str: stores the student's address.
        address = input("Address: ")

        # str: stores the Student ID.
        student_id = input("Student ID: ")

        # Create a Student object using the information entered.
        student = Student(full_name, age, address, student_id)

        # append() adds the Student object to the students list.
        students.append(student)

    # sorted() creates a new list sorted according to the student's age.
    # key=lambda student: student.age tells Python to sort by age.
    sorted_students_age = sorted(students, key=lambda student: student.age)

    sorted_students_id = sorted(students, key=lambda student: student.student_id)

    print("\n===== STUDENTS SORTED BY AGE =====")

    # Display each student after sorting.
    for student in sorted_students_age:
        student.display_information()


    print("\n===== STUDENTS SORTED BY ID =====")


    # Display each student after sorting.
    for student in sorted_students_id:
        student.display_information()

# This checks whether this Python file is being run directly.
if __name__ == "__main__":
    main()