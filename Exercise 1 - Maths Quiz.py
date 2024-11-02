import tkinter as tk
from tkinter import messagebox
import random

# Function to display the menu for difficulty selection
def displayMenu():
    menu_frame.pack(fill='both', expand=True)
    for widget in menu_frame.winfo_children():
        widget.destroy()  # Clear previous widgets

    tk.Label(menu_frame, text="DIFFICULTY LEVEL", font=("Arial", 16, "bold"), bg="lightblue").pack(pady=10)
    tk.Button(menu_frame, text="1. Easy", command=lambda: startQuiz(1), **button_style).pack(pady=5)
    tk.Button(menu_frame, text="2. Moderate", command=lambda: startQuiz(2), **button_style).pack(pady=5)
    tk.Button(menu_frame, text="3. Advanced", command=lambda: startQuiz(3), **button_style).pack(pady=5)

# Function to generate random integers based on difficulty
def randomInt(difficulty):
    if difficulty == 1:
        return random.randint(0, 9)
    elif difficulty == 2:
        return random.randint(10, 99)
    elif difficulty == 3:
        return random.randint(100, 999)

# Function to decide whether to add or subtract
def decideOperation():
    return random.choice(['+', '-'])

# Function to display a problem and get the user's answer
def displayProblem(difficulty):
    global correct_answer
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()
    correct_answer = num1 + num2 if operation == '+' else num1 - num2

    question_label.config(text=f"{num1} {operation} {num2} = ?")
    answer_entry.delete(0, tk.END)  # Clear previous answer

# Function to check the user's answer
def checkAnswer():
    global score, attempts
    user_answer = answer_entry.get()
    try:
        user_answer = int(user_answer)
        if user_answer == correct_answer:
            messagebox.showinfo("Result", "Correct!")
            score += 10 if attempts == 1 else 5
            nextQuestion()
        else:
            attempts -= 1
            if attempts > 0:
                messagebox.showerror("Result", "Incorrect, try again.")
            else:
                messagebox.showerror("Result", "Incorrect, moving to the next question.")
                nextQuestion()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

# Function to proceed to the next question or end quiz
def nextQuestion():
    global question_count, attempts
    question_count += 1
    attempts = 2
    if question_count > 10:
        displayResults(score)
    else:
        displayProblem(current_difficulty)

# Function to start the quiz
def startQuiz(difficulty):
    global score, question_count, current_difficulty, attempts
    menu_frame.pack_forget()  # Hide the menu
    quiz_frame.pack(fill='both', expand=True)  # Show the quiz frame
    score = 0
    question_count = 1
    current_difficulty = difficulty
    attempts = 2
    displayProblem(difficulty)

# Function to display the final results
def displayResults(score):
    quiz_frame.pack_forget()  # Hide the quiz frame
    result_frame.pack(fill='both', expand=True)  # Show the results frame
    result_label.config(text=f"Your final score is: {score} out of 100")

# Main application setup
root = tk.Tk()
root.title("Maths Quiz")
root.geometry("400x400")

# Set background color
root.configure(bg="lightblue")

# Title Label
title_label = tk.Label(root, text="Maths Quiz", font=("Arial", 24, "bold"), bg="lightblue", fg="darkblue")
title_label.pack(pady=20)

# Define button style
button_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#45a049",
    "activeforeground": "white",
    "bd": 2,
    "relief": "raised",
    "width": 15
}

# Create frames for menu, quiz, and results
menu_frame = tk.Frame(root, bg="lightblue")
quiz_frame = tk.Frame(root, bg="lightblue")
result_frame = tk.Frame(root, bg="lightblue")

# Widgets for quiz frame
question_label = tk.Label(quiz_frame, text="", font=("Arial", 14), bg="lightblue")
question_label.pack(pady=20)
answer_entry = tk.Entry(quiz_frame)
answer_entry.pack(pady=10)
tk.Button(quiz_frame, text="Submit", command=checkAnswer, **button_style).pack(pady=5)

# Widgets for results frame
result_label = tk.Label(result_frame, text="", font=("Arial", 14), bg="lightblue")
result_label.pack(pady=20)
tk.Button(result_frame, text="Play Again", command=displayMenu, **button_style).pack(pady=5)

# Variables to keep track of score and current question
current_difficulty = 1
score = 0
question_count = 1
attempts = 2

# Start the quiz
displayMenu()
root.mainloop()




