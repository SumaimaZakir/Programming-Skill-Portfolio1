import tkinter as tk
import random

# List of jokes
jokes = [
    "Why did the chicken cross the road?To get to the other side.",
    "What happens if you boil a clown?You get a laughing stock.",
    "Why did the car get a flat tire?Because there was a fork in the road!",
    # Add other jokes here...
]

# Variable to store the punchline
current_punchline = ""


def tell_joke():
    global current_punchline
    # Choose a random joke
    joke = random.choice(jokes)

    # Split the joke into setup and punchline
    setup, punchline = joke.split('?')
    current_punchline = punchline.strip()

    # Update the joke setup and punchline labels
    setup_label.config(text=setup + "?")
    punchline_label.config(text="")
    punchline_button.config(state="normal")


def show_punchline():
    # Display the stored punchline
    punchline_label.config(text=current_punchline)
    punchline_button.config(state="disabled")


# Set up the tkinter window
root = tk.Tk()
root.title("Joke Teller")
root.geometry("400x300")

# Load background image
try:
    background_image = tk.PhotoImage(file="background.png")  # Replace with your image file name
    # Display the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
except Exception as e:
    print("Error loading background image:", e)
    root.config(bg="#ADD8E6")  # Fallback background color if image loading fails

# Joke setup label with transparent background
setup_label = tk.Label(root, text="Click the button to hear a joke!", font=("Helvetica", 14), bg="#ADD8E6")
setup_label.pack(pady=20)

# Punchline label with transparent background
punchline_label = tk.Label(root, text="", font=("Helvetica", 14, "italic"), bg="#ADD8E6")
punchline_label.pack(pady=10)

# Button style dictionary
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#ff6600",        # Orange background
    "fg": "white",           # White text
    "activebackground": "#ff4500",  # Darker orange on hover
    "activeforeground": "white",
    "bd": 3,                 # Border thickness
    "relief": "raised",
    "width": 15
}

# Button to get a new joke with enhanced style
joke_button = tk.Button(root, text="Tell me a joke", command=tell_joke, **button_style)
joke_button.pack(pady=10)

# Button to show the punchline with enhanced style
punchline_button = tk.Button(root, text="Show punchline", command=show_punchline, state="disabled", **button_style)
punchline_button.pack(pady=10)

root.mainloop()




