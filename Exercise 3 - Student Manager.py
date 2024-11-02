import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import for combobox

# Define the file path
file_path = "studentMarks.txt"

# Load students' data from the file
def load_data():
    students = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line (number of students)
        for row in reader:
            student_id = int(row[0])
            name = row[1]
            marks = list(map(int, row[2:5]))  # coursework marks
            exam_mark = int(row[5])  # exam mark
            students.append({
                "id": student_id,
                "name": name,
                "marks": marks,
                "exam": exam_mark
            })
    return students

# Calculate the total and percentage marks
def calculate_scores(student):
    total_coursework = sum(student["marks"])
    total_marks = total_coursework + student["exam"]
    percentage = (total_marks / 160) * 100
    return total_coursework, total_marks, percentage

# Determine the grade based on percentage
def get_grade(percentage):
    if percentage >= 70:
        return 'A'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

# Display all student records
def view_all_students():
    output_text.delete(1.0, tk.END)  # Clear output
    total_percentage = 0
    for student in students:
        total_coursework, total_marks, percentage = calculate_scores(student)
        grade = get_grade(percentage)
        output_text.insert(tk.END, f"Name: {student['name']}, ID: {student['id']}\n")
        output_text.insert(tk.END, f"Coursework: {total_coursework}, Exam: {student['exam']}\n")
        output_text.insert(tk.END, f"Overall Percentage: {percentage:.2f}%, Grade: {grade}\n\n")
        total_percentage += percentage
    avg_percentage = total_percentage / len(students)
    output_text.insert(tk.END, f"Total Students: {len(students)}, Average Percentage: {avg_percentage:.2f}%\n")

# View a specific student record
def view_individual_student():
    selected_student_name = student_combobox.get()
    student = next((s for s in students if s["name"] == selected_student_name), None)
    output_text.delete(1.0, tk.END)  # Clear output
    if student:
        total_coursework, total_marks, percentage = calculate_scores(student)
        grade = get_grade(percentage)
        output_text.insert(tk.END, f"\nName: {student['name']}, ID: {student['id']}\n")
        output_text.insert(tk.END, f"Coursework: {total_coursework}, Exam: {student['exam']}\n")
        output_text.insert(tk.END, f"Overall Percentage: {percentage:.2f}%, Grade: {grade}\n\n")
    else:
        messagebox.showerror("Error", "Student not found.")

# Show the student with the highest score
def show_highest_score():
    highest_student = max(students, key=lambda s: calculate_scores(s)[1])
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Student with highest total score:\n")
    display_student_info(highest_student)

# Show the student with the lowest score
def show_lowest_score():
    lowest_student = min(students, key=lambda s: calculate_scores(s)[1])
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Student with lowest total score:\n")
    display_student_info(lowest_student)

# Display student info in output_text widget
def display_student_info(student):
    total_coursework, total_marks, percentage = calculate_scores(student)
    grade = get_grade(percentage)
    output_text.insert(tk.END, f"\nName: {student['name']}, ID: {student['id']}\n")
    output_text.insert(tk.END, f"Coursework: {total_coursework}, Exam: {student['exam']}\n")
    output_text.insert(tk.END, f"Overall Percentage: {percentage:.2f}%, Grade: {grade}\n\n")

# Load student data
students = load_data()
student_names = [student["name"] for student in students]  # Get list of student names for dropdown

# Set up the Tkinter window
root = tk.Tk()
root.title("Student Manager")
root.geometry("800x500")  # Set the window size to 800x500 pixels
root.configure(bg="#E6E6FA")  # Set the background color of the main window

# Heading Label
heading_label = tk.Label(root, text="Student Manager", font=("Helvetica", 16, "bold"), bg="#9370DB")
heading_label.pack(pady=10)

# Horizontal frame for the buttons
button_frame = tk.Frame(root, bg="#f0f0f0")  # Set the background color of the button frame
button_frame.pack(pady=10)

# Add buttons horizontally
button_view_all = tk.Button(button_frame, text="View All Student Records", command=view_all_students)
button_view_all.pack(side=tk.LEFT, padx=5)

# Dropdown (Combobox) for selecting an individual student
student_combobox = ttk.Combobox(button_frame, values=student_names, width=20)
student_combobox.set("Select Student")
student_combobox.pack(side=tk.LEFT, padx=5)

button_view_individual = tk.Button(button_frame, text="View Individual Record", command=view_individual_student)
button_view_individual.pack(side=tk.LEFT, padx=5)

button_highest_score = tk.Button(button_frame, text="Show Highest Total Score", command=show_highest_score)
button_highest_score.pack(side=tk.LEFT, padx=5)

button_lowest_score = tk.Button(button_frame, text="Show Lowest Total Score", command=show_lowest_score)
button_lowest_score.pack(side=tk.LEFT, padx=5)

button_exit = tk.Button(button_frame, text="Exit", command=root.quit)
button_exit.pack(side=tk.LEFT, padx=5)

# Output text area
output_text = tk.Text(root, wrap="word", width=60, height=20, bg="#ffffff")  # Set background color of the text area
output_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()



