from database import create_table
from student_manager import add_student, view_student, add_subject, view_subject, add_lecturer, view_lecturer


def menu():
    print("\n==== College Enrollment Manager ====")
    print("1. Add Student")
    print("2. View All Student")
    print("3. Add Subjects")
    print("4. View All Subjects")
    print("5. Add Lecturers")
    print("6. View All Lecturers")
    print("7. Exit")


def main():
    while True:
        menu()
        choice = input("Select an option (1-5): ")
        if choice == '1':
            F_name = input("Enter student's First name: ")
            L_name = input("Enter student's Last name: ")
            B_date = input("Enter the student's Date of Birth: ")
            add_student(F_name, L_name, B_date)
           
        elif choice == '2':
            students = view_student()
            for student in students:
                print(student)

        elif choice == '3':
             Subject_code = input("Enter Subject Code: ")
             Subject_unit = input("Enter Subject_unit: ")
             Subject_udsc = input("Enter Subject_udsc: ")
             add_subject(Subject_code, Subject_unit, Subject_udsc)

        elif choice == '4':
            subjects = view_subject()
            for subject in subjects:
                print(subject)

        elif choice == '5':
            L_firstname = input("Enter Lecturer First Name: ")
            L_lastname = input("Enter Lecturer Last Name: ")
            L_email = input("Enter Lecturer email: ")
            L_address = input("Enter Lecturer address: ")
            add_lecturer(L_firstname, L_lastname, L_email, L_address)
        
        elif choice == '6':
            Lecturers = view_lecturer()
            for Lecturer in Lecturers:
                print(Lecturer)

        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
