class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password

    def verify_login(self, email, password):
        return self.email == email and self.password == password


class Student(User):
    def __init__(self, student_id, name, email, password):
        super().__init__(student_id, name, email, password)
        self.student_id = student_id
        self.courses = []
        self.submissions = {}

    def enroll_course(self, course):
        if course.add_student(self):
            self.courses.append(course)
            print("Successfully enrolled in", course.course_title)
        else:
            print("Cannot enroll. Course is full or you are already enrolled.")

    def submit_assignment(self, assignment):
        content = input("Enter your assignment: ")

        if content.strip() == "":
            print("Assignment cannot be empty.")
            return

        self.submissions[assignment.title] = {
            "content": content,
            "grade": None
        }

        assignment.submissions.append(self)
        print("Assignment submitted successfully.")

    def view_grades(self):
        print("\n--- My Grades ---")

        if not self.submissions:
            print("No submissions found.")
            return

        for title, submission in self.submissions.items():
            grade = submission["grade"]

            if grade is None:
                print(title, "- Not graded")
            else:
                print(title, "-", grade)


class Lecturer(User):
    def __init__(self, lecturer_id, name, email, password, department):
        super().__init__(lecturer_id, name, email, password)
        self.lecturer_id = lecturer_id
        self.department = department

    def create_course(self, code, title, capacity):
        return Course(code, title, capacity, self)

    def assign_assignment(self, course):
        title = input("Assignment title: ")
        description = input("Assignment description: ")

        assignment = Assignment(title, description, course)
        course.assignments.append(assignment)

        print("Assignment created successfully.")

    def assign_grade(self, student, assignment):
        if assignment.title not in student.submissions:
            print("Student has not submitted this assignment.")
            return

        try:
            grade = float(input("Enter grade (0-100): "))

            if grade < 0 or grade > 100:
                print("Grade must be between 0 and 100.")
                return

            student.submissions[assignment.title]["grade"] = grade
            print("Grade assigned successfully.")

        except ValueError:
            print("Please enter a valid number.")


class Course:
    def __init__(self, course_code, course_title, capacity, lecturer):
        self.course_code = course_code
        self.course_title = course_title
        self.capacity = capacity
        self.lecturer = lecturer
        self.students = []
        self.assignments = []

    def add_student(self, student):
        if student in self.students:
            return False

        if len(self.students) >= self.capacity:
            return False

        self.students.append(student)
        return True

    def seats_available(self):
        return self.capacity - len(self.students)

    def display(self):
        print(
            self.course_code,
            "-",
            self.course_title,
            "| Lecturer:",
            self.lecturer.name,
            "| Seats:",
            self.seats_available()
        )


class Assignment:
    def __init__(self, title, description, course):
        self.title = title
        self.description = description
        self.course = course
        self.submissions = []


# --------------------------------------------------
# STUDENT MANAGEMENT SYSTEM
# --------------------------------------------------

users = []
courses = []


def find_course(code):
    for course in courses:
        if course.course_code.lower() == code.lower():
            return course

    return None


def student_menu(student):
    while True:
        print("\n==============================")
        print("       STUDENT MENU")
        print("==============================")
        print("1. View Courses")
        print("2. Enroll in Course")
        print("3. View Assignments")
        print("4. Submit Assignment")
        print("5. View Grades")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print("\n--- Available Courses ---")

            for course in courses:
                course.display()

        elif choice == "2":
            print("\n--- Available Courses ---")

            for course in courses:
                course.display()

            code = input("\nEnter course code: ")
            course = find_course(code)

            if course:
                student.enroll_course(course)
            else:
                print("Course not found.")

        elif choice == "3":
            print("\n--- Assignments ---")

            found = False

            for course in student.courses:
                for assignment in course.assignments:
                    found = True
                    print(
                        course.course_code,
                        "-",
                        assignment.title,
                        ":",
                        assignment.description
                    )

            if not found:
                print("No assignments available.")

        elif choice == "4":
            if not student.courses:
                print("You are not enrolled in any course.")
                continue

            print("\n--- Assignments ---")

            assignments = []

            for course in student.courses:
                for assignment in course.assignments:
                    assignments.append(assignment)

            if not assignments:
                print("No assignments available.")
                continue

            for i, assignment in enumerate(assignments, 1):
                print(i, ".", assignment.title)

            try:
                number = int(input("Select assignment: "))

                if number < 1 or number > len(assignments):
                    print("Invalid assignment.")
                    continue

                student.submit_assignment(assignments[number - 1])

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            student.view_grades()

        elif choice == "0":
            print("Logged out.")
            break

        else:
            print("Invalid option.")


def lecturer_menu(lecturer):
    while True:
        print("\n==============================")
        print("       LECTURER MENU")
        print("==============================")
        print("1. View My Courses")
        print("2. Create Course")
        print("3. Assign Assignment")
        print("4. Grade Student")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print("\n--- My Courses ---")

            my_courses = [
                course for course in courses
                if course.lecturer == lecturer
            ]

            if not my_courses:
                print("No courses found.")

            for course in my_courses:
                course.display()

                print("Students:")

                for student in course.students:
                    print(" -", student.name)

        elif choice == "2":
            code = input("Course code: ")
            title = input("Course title: ")

            try:
                capacity = int(input("Course capacity: "))

                course = lecturer.create_course(
                    code,
                    title,
                    capacity
                )

                courses.append(course)

                print("Course created successfully.")

            except ValueError:
                print("Capacity must be a number.")

        elif choice == "3":
            my_courses = [
                course for course in courses
                if course.lecturer == lecturer
            ]

            if not my_courses:
                print("No courses available.")
                continue

            print("\n--- My Courses ---")

            for course in my_courses:
                print(course.course_code, "-", course.course_title)

            code = input("Enter course code: ")
            course = find_course(code)

            if course and course.lecturer == lecturer:
                lecturer.assign_assignment(course)
            else:
                print("Course not found.")

        elif choice == "4":
            my_courses = [
                course for course in courses
                if course.lecturer == lecturer
            ]

            for course in my_courses:
                for assignment in course.assignments:

                    if not assignment.submissions:
                        continue

                    print("\nAssignment:", assignment.title)

                    for student in assignment.submissions:
                        print(
                            "Student:",
                            student.name
                        )

                        print(
                            "Submission:",
                            student.submissions[
                                assignment.title
                            ]["content"]
                        )

                        lecturer.assign_grade(
                            student,
                            assignment
                        )

        elif choice == "0":
            print("Logged out.")
            break

        else:
            print("Invalid option.")


def login():
    print("\n========== LOGIN ==========")

    email = input("Email: ")
    password = input("Password: ")

    for user in users:

        if user.verify_login(email, password):

            print("\nLogin successful!")
            print("Welcome,", user.name)

            if isinstance(user, Student):
                student_menu(user)

            elif isinstance(user, Lecturer):
                lecturer_menu(user)

            return

    print("Invalid email or password.")


# --------------------------------------------------
# SAMPLE DATA
# --------------------------------------------------

student = Student(
    "S001",
    "John Student",
    "student@college.com",
    "student123"
)

lecturer = Lecturer(
    "L001",
    "Jane Lecturer",
    "lecturer@college.com",
    "lecturer123",
    "Software Engineering"
)

users.append(student)
users.append(lecturer)


course1 = lecturer.create_course(
    "SE101",
    "Object Oriented Programming",
    30
)

course2 = lecturer.create_course(
    "SE102",
    "Software Design",
    25
)

courses.append(course1)
courses.append(course2)

course1.assignments.append(
    Assignment(
        "OOP Project",
        "Develop a CLI application using OOP.",
        course1
    )
)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    while True:

        print("\n================================")
        print("   STUDENT MANAGEMENT SYSTEM")
        print("================================")
        print("1. Login")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            login()

        elif choice == "0":
            print("\nThank you for using the system!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()