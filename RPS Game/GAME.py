import tkinter as tk
import random

class RockPaperScissors:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")

        # Custom colors
        self.background_color = "#D3D3D3"  # Light grey background
        self.button_color = "#4CAF50"  # Green for buttons
        self.button_hover_color = "#45a049"  # Darker green for button hover
        self.button_active_color = "#3e8e41"  # Even darker green for button click
        self.label_color = "#333333"  # Dark grey for labels and text
        self.result_color = "#FF7F7F"  # Blue for result text

        # Configure window background color and size
        master.configure(bg=self.background_color)
        master.geometry("400x300")  # Set initial size of the window

        # Choices available in the game
        self.choices = ["Rock", "Paper", "Scissors"]

        # Styling for labels and buttons
        self.label_font = ("Helvetica", 14, "bold")
        self.button_font = ("Helvetica", 12, "bold")

        # Main frame
        self.frame = tk.Frame(master, bg=self.background_color)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Title label
        self.title_label = tk.Label(self.frame, text="Rock Paper Scissors By PARTH", fg=self.label_color, bg=self.background_color, font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=20)

        # Buttons frame
        self.buttons_frame = tk.Frame(self.frame, bg=self.background_color)
        self.buttons_frame.pack()

        # Buttons
        self.rock_button = tk.Button(self.buttons_frame, text="Rock", command=lambda: self.play("Rock"), bg=self.button_color, fg="white", font=self.button_font, width=10)
        self.rock_button.config(activebackground=self.button_active_color, activeforeground="white")
        self.rock_button.bind("<Enter>", lambda e: self.rock_button.config(bg=self.button_hover_color))
        self.rock_button.bind("<Leave>", lambda e: self.rock_button.config(bg=self.button_color))
        self.rock_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.paper_button = tk.Button(self.buttons_frame, text="Paper", command=lambda: self.play("Paper"), bg=self.button_color, fg="white", font=self.button_font, width=10)
        self.paper_button.config(activebackground=self.button_active_color, activeforeground="white")
        self.paper_button.bind("<Enter>", lambda e: self.paper_button.config(bg=self.button_hover_color))
        self.paper_button.bind("<Leave>", lambda e: self.paper_button.config(bg=self.button_color))
        self.paper_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.scissors_button = tk.Button(self.buttons_frame, text="Scissors", command=lambda: self.play("Scissors"), bg=self.button_color, fg="white", font=self.button_font, width=10)
        self.scissors_button.config(activebackground=self.button_active_color, activeforeground="white")
        self.scissors_button.bind("<Enter>", lambda e: self.scissors_button.config(bg=self.button_hover_color))
        self.scissors_button.bind("<Leave>", lambda e: self.scissors_button.config(bg=self.button_color))
        self.scissors_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Result message box
        self.result_label = tk.Label(self.frame, text="", fg=self.result_color, bg=self.background_color, font=self.label_font)
        self.result_label.pack(pady=20)

    def play(self, player_choice):
        # Computer makes a random choice
        computer_choice = random.choice(self.choices)

        # Determine the winner
        if player_choice == computer_choice:
            result = "It's a tie!"
        elif (player_choice == "Rock" and computer_choice == "Scissors") or \
             (player_choice == "Paper" and computer_choice == "Rock") or \
             (player_choice == "Scissors" and computer_choice == "Paper"):
            result = "You win!"
        else:
            result = "Computer wins!"

        # Update the result message
        self.result_label.config(text=result)

# Instantiate the GUI and start the main event loop
if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()
