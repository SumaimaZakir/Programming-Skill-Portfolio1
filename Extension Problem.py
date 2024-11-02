import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
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


# Save students' data back to the file
def save_data():
    with open(file_path, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Mark1", "Mark2", "Mark3", "Exam"])  # Write header
        for student in students:
            writer.writerow([student["id"], student["name"]] + student["marks"] + [student["exam"]])


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


# Sort student records
def sort_students():
    sort_order = simpledialog.askstring("Sort Order", "Enter 'asc' for ascending or 'desc' for descending:")
    if sort_order not in ['asc', 'desc']:
        messagebox.showerror("Error", "Invalid sort order.")
        return

    ascending = sort_order == 'asc'
    students.sort(key=lambda s: s['name'], reverse=not ascending)  # Sort by name
    view_all_students()  # Refresh display


# Add a student record
def add_student():
    new_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    if new_id is None:
        return
    name = simpledialog.askstring("Student Name", "Enter Student Name:")
    if name is None:
        return
    marks = []
    for i in range(3):  # Assuming 3 coursework marks
        mark = simpledialog.askinteger("Coursework Mark", f"Enter Coursework Mark {i + 1}:")
        if mark is None:
            return
        marks.append(mark)
    exam_mark = simpledialog.askinteger("Exam Mark", "Enter Exam Mark:")
    if exam_mark is None:
        return

    students.append({
        "id": new_id,
        "name": name,
        "marks": marks,
        "exam": exam_mark
    })
    save_data()  # Save to file
    view_all_students()  # Refresh display


# Delete a student record
def delete_student():
    selected_student_name = student_combobox.get()
    student_to_delete = next((s for s in students if s["name"] == selected_student_name), None)
    if student_to_delete:
        students.remove(student_to_delete)
        save_data()  # Save changes to file
        view_all_students()  # Refresh display
        messagebox.showinfo("Success", f"Deleted student: {student_to_delete['name']}")
    else:
        messagebox.showerror("Error", "Student not found.")


# Update a student's record
def update_student():
    selected_student_name = student_combobox.get()
    student_to_update = next((s for s in students if s["name"] == selected_student_name), None)
    if not student_to_update:
        messagebox.showerror("Error", "Student not found.")
        return

    # Display a sub-menu for updates
    update_field = simpledialog.askstring("Update Field", "What do you want to update? (name/marks/exam)")
    if update_field == "name":
        new_name = simpledialog.askstring("New Name", "Enter new name:")
        student_to_update['name'] = new_name
    elif update_field == "marks":
        for i in range(3):  # Assuming 3 coursework marks
            new_mark = simpledialog.askinteger("New Coursework Mark", f"Enter new mark for Coursework {i + 1}:")
            if new_mark is None:
                return
            student_to_update['marks'][i] = new_mark
    elif update_field == "exam":
        new_exam_mark = simpledialog.askinteger("New Exam Mark", "Enter new exam mark:")
        student_to_update['exam'] = new_exam_mark

    save_data()  # Save changes to file
    view_all_students()  # Refresh display
    messagebox.showinfo("Success", "Student record updated.")


# Load student data
students = load_data()
student_names = [student["name"] for student in students]  # Get list of student names for dropdown

# Set up the Tkinter window
root = tk.Tk()
root.title("Student Manager")
root.geometry("1000x600")  # Set the window size to 800x600 pixels
root.configure(bg="#E6E6FA")  # Set the background color of the main window

# Heading Label
heading_label = tk.Label(root, text="Student Manager", font=("Helvetica", 16, "bold"), bg="#9370DB")
heading_label.pack(pady=10)

# Frame for the buttons (first row)
button_frame1 = tk.Frame(root, bg="#f0f0f0")  # Set the background color of the button frame
button_frame1.pack(pady=10)

# Add buttons in the first row
button_view_all = tk.Button(button_frame1, text="View All Student Records", command=view_all_students)
button_view_all.pack(side=tk.LEFT, padx=5)

# Dropdown (Combobox) for selecting an individual student
student_combobox = ttk.Combobox(button_frame1, values=student_names, width=20)
student_combobox.set("Select Student")
student_combobox.pack(side=tk.LEFT, padx=5)

button_view_individual = tk.Button(button_frame1, text="View Individual Record", command=view_individual_student)
button_view_individual.pack(side=tk.LEFT, padx=5)

# Frame for the buttons (second row)
button_frame2 = tk.Frame(root, bg="#f0f0f0")  # Set the background color of the button frame
button_frame2.pack(pady=10)

# Add buttons in the second row
button_highest_score = tk.Button(button_frame2, text="Show Highest Total Score", command=show_highest_score)
button_highest_score.pack(side=tk.LEFT, padx=5)

button_lowest_score = tk.Button(button_frame2, text="Show Lowest Total Score", command=show_lowest_score)
button_lowest_score.pack(side=tk.LEFT, padx=5)

button_sort = tk.Button(button_frame2, text="Sort Student Records", command=sort_students)
button_sort.pack(side=tk.LEFT, padx=5)

button_add = tk.Button(button_frame2, text="Add Student Record", command=add_student)
button_add.pack(side=tk.LEFT, padx=5)

button_delete = tk.Button(button_frame2, text="Delete Student Record", command=delete_student)
button_delete.pack(side=tk.LEFT, padx=5)

button_update = tk.Button(button_frame2, text="Update Student Record", command=update_student)
button_update.pack(side=tk.LEFT, padx=5)

button_exit = tk.Button(button_frame2, text="Exit", command=root.quit)
button_exit.pack(side=tk.LEFT, padx=5)

# Output text area
output_text = tk.Text(root, wrap="word", width=60, height=20, bg="#ffffff")  # Set background color of the text area
output_text.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
