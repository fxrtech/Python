import tkinter as tk
from tkinter import messagebox

def show_smiley():
    messagebox.showinfo("Result", "😊 You're happy!")

def show_frowning():
    messagebox.showinfo("Result", "☹️ You're not happy.")

# Create the main window
root = tk.Tk()
root.title("Are You Happy?")

# Create buttons
yes_button = tk.Button(root, text="Yes", command=show_smiley)
no_button = tk.Button(root, text="No", command=show_frowning)

# Pack buttons into the window
yes_button.pack()
no_button.pack()

# Start the GUI event loop
root.mainloop()
