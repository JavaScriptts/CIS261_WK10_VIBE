#Jay-Jay Buenavista
#CIS261
#VIBE CODING

import os
import sys
import termios
import tty

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_grades.txt")


class Student:
    def __init__(self, name, student_id, test1, test2, test3):
        self.name = name
        self.id = student_id
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self):
        return (self.test1 + self.test2 + self.test3) / 3

    def calculate_grade(self):
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"

    def to_record(self):
        return (
            f"{self.name}|{self.id}|{self.test1:.2f}|{self.test2:.2f}|"
            f"{self.test3:.2f}|{self.average:.2f}|{self.grade}"
        )

    @classmethod
    def from_record(cls, record):
        parts = record.strip().split("|")
        if len(parts) != 7:
            raise ValueError("Invalid record format")

        name, student_id, test1, test2, test3, average, grade = parts
        student = cls(name, student_id, test1, test2, test3)
        student.average = float(average)
        student.grade = grade
        return student


def get_valid_text(prompt, field_name):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be empty. Please try again.")


def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            return value
        except ValueError:
            print("Invalid number. Please enter a numeric score.")


def load_students():
    students = []

    if not os.path.exists(DATA_FILE):
        print("No saved records found. A new file will be created when you save.")
        return students

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                record = line.strip()
                if not record:
                    continue

                try:
                    student = Student.from_record(record)
                    students.append(student)
                except ValueError:
                    print(f"Skipping invalid record on line {line_number}: {record}")

        if students:
            print(f"Loaded {len(students)} student record(s) from {os.path.basename(DATA_FILE)}.")
        return students

    except OSError as exc:
        print(f"Error loading file: {exc}")
        return []


def save_students(students):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_record() + "\n")
        print(f"Student records saved to {os.path.basename(DATA_FILE)}.")
    except OSError as exc:
        print(f"Error saving file: {exc}")


def add_student(students):
    name = get_valid_text("Enter student name: ", "Student name")
    student_id = get_valid_text("Enter student ID: ", "Student ID")

    test1 = get_valid_float("Enter Test 1 score: ")
    test2 = get_valid_float("Enter Test 2 score: ")
    test3 = get_valid_float("Enter Test 3 score: ")

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)

    print(f"Student {name} added successfully.")
    save_students(students)


def display_students(students):
    if not students:
        print("No student records available.")
        return

    print("\nStudent Records")
    print("-" * 120)
    header = f"{'Name':<18} {'ID':<12} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>10} {'Grade':>6}"
    print(header)
    print("-" * 120)

    for student in students:
        print(
            f"{student.name:<18} {student.id:<12} {student.test1:>8.2f} "
            f"{student.test2:>8.2f} {student.test3:>8.2f} {student.average:>10.2f} {student.grade:>6}"
        )

    print("-" * 120)


def display_class_statistics(students):
    if not students:
        print("No student records available to calculate class statistics.")
        return

    averages = [student.average for student in students]
    highest_average = max(averages)
    lowest_average = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print("-" * 40)
    print(f"Highest Average: {highest_average:.2f}")
    print(f"Lowest Average:  {lowest_average:.2f}")
    print(f"Class Average:   {class_average:.2f}")
    print("-" * 40)


def search_student(students, search_name):
    matches = []
    search_term = search_name.lower()

    for student in students:
        if search_term in student.name.lower():
            matches.append(student)

    if not matches:
        print(f"No student found matching '{search_name}'.")
        return

    print(f"\nSearch results for '{search_name}':")
    display_students(matches)


def read_key():
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return "ESC" if key == "\x1b" else key
    except (termios.error, OSError):
        fallback = input().strip()
        if not fallback:
            return ""
        return fallback[0]


def get_menu_choice():
    print("\nStudent Grade Calculator")
    print("1. Add student")
    print("2. Display all students")
    print("3. Search for a student")
    print("4. Display class statistics")
    print("5. Save records")
    print("6. Exit")
    print("ESC. Exit immediately")

    while True:
        choice = read_key()
        if choice in {"1", "2", "3", "4", "5", "6", "ESC"}:
            return choice
        print("Invalid option. Please choose 1, 2, 3, 4, 5, 6, or press ESC.")


def main():
    students = load_students()

    while True:
        choice = get_menu_choice()

        if choice == "ESC" or choice == "6":
            print("Exiting Student Grade Calculator. Goodbye!")
            save_students(students)
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            name = get_valid_text("Enter student name to search: ", "Student name")
            search_student(students, name)
        elif choice == "4":
            display_class_statistics(students)
        elif choice == "5":
            save_students(students)


if __name__ == "__main__":
    main()
