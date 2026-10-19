# ===============================================
# CBSE CLASS 12 COMPUTER SCIENCE PROJECT
# PROGRAM: Color Memory Game
# AUTHOR: Avi
# ===============================================
# DESCRIPTION:
# A color-guessing memory game built using Python's Tkinter module.
# The player must type the COLOR of the displayed word (not the word itself)
# within a fixed time limit. Scores are tracked and a high score is saved.
# ===============================================

# --- IMPORTS ---
import tkinter as tk
import random
from tkinter import ttk     # OUT OF SYLLABUS: ttk is an advanced GUI toolkit for styled widgets

# --- GAME CONSTANTS ---
font_colors = ['Red', 'Blue', 'Green', 'Yellow', 'Orange',
               'Purple', 'Brown', 'Pink', 'Gray', 'White']

words = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Brown', 'Pink',
         'Black', 'White', 'Gray', 'Cyan', 'Magenta', 'Lime', 'Maroon', 'Teal']


difficulty_levels = {
    "Very Easy": 1.5,
    "Easy": 1.2,
    "Medium": 0.9,
    "Hard": 0.6,
    "Very Hard": 0.3
}

# --- GLOBAL VARIABLES ---
score = 0
high_score = 0
time_left = 30.0
current_color = ''
last_color = ''
actual_word = ''
timer_running = False
game_started = False
reveal_time = 1.0
countdown_interval = 10  # milliseconds

# =====================================================
# FUNCTION: load_high_score
# PURPOSE: To read the saved high score from a text file
# TOPIC: File Handling (CBSE Syllabus)
# =====================================================
def load_high_score():
    global high_score
    try:
        file = open("highscore.txt", "r")  # open file in read mode
        data = file.read().strip()
        high_score = int(data) if data.isdigit() else 0
        file.close()
    except FileNotFoundError:
        # If file not found, create it and set high score = 0
        file = open("highscore.txt", "w")
        file.write("0")
        file.close()
        high_score = 0

# =====================================================
# FUNCTION: save_high_score
# PURPOSE: To write the current high score to a file
# TOPIC: File Handling (CBSE Syllabus)
# =====================================================
def save_high_score():
    file = open("highscore.txt", "w")
    file.write(str(high_score))
    file.close()

# =====================================================
# FUNCTION: countdown
# PURPOSE: Runs the game timer and updates time bar(inspired)
# TOPIC: Functions, Conditionals, Recursion
# =====================================================
def countdown():
    global time_left, timer_running
    if timer_running and time_left > 0:
        time_left -= countdown_interval / 1000
        time_left_label.config(text=f"Time left: {int(time_left)}")
        timer_bar['value'] = time_left
        window.after(countdown_interval, countdown)  # OUT OF SYLLABUS: GUI timing function
    elif time_left <= 0:
        time_left_label.config(text="Time left: 0")
        timer_bar['value'] = 0
        end_game()

# =====================================================
# FUNCTION: on_start_click
# PURPOSE: Starts the game after difficulty selection
# TOPIC: GUI Events, Conditional Statements
# =====================================================
def on_start_click():
    global game_started, reveal_time
    selected_level = difficulty_var.get()
    if selected_level not in difficulty_levels:
        return

    reveal_time = difficulty_levels[selected_level]
    game_started = True
    load_high_score()

    # Hide initial screen
    start_button.pack_forget()
    level_menu.pack_forget()
    retry_button.pack_forget()

    # Start transition messages
    entry.config(state='disabled')
    word_label.config(text="Ready...", fg="black")
    window.after(1000, lambda: word_label.config(text="Go!", fg="black"))
    window.after(2000, start_round)

# =====================================================
# FUNCTION: retry_game
# PURPOSE: Resets all game variables and restarts
# =====================================================
def retry_game():
    global score, time_left, last_color, game_started, timer_running

    score = 0
    time_left = 30.0
    last_color = ''
    timer_running = False
    game_started = False

    # Reset UI
    score_label.config(text="Score: 0")
    time_left_label.config(text="Time left: 30")
    timer_bar['value'] = 30
    word_label.config(text="", font=('Helvetica', 40))
    entry.delete(0, tk.END)
    entry.config(state='disabled')

    # Show start screen again
    start_button.pack(pady=10)
    level_menu.pack(pady=10)
    retry_button.pack_forget()

# =====================================================
# FUNCTION: start_round
# PURPOSE: Displays a new random word in a color
# TOPIC: Random Module, Lists
# =====================================================
def start_round():
    global current_color, actual_word, timer_running, last_color

    entry.config(state='disabled')
    timer_running = False

    actual_word = random.choice(words)
    possible_colors = [c for c in font_colors if c != actual_word and c != last_color]

    if not possible_colors:
        end_game()
        return

    current_color = random.choice(possible_colors)
    last_color = current_color

    word_label.config(text=actual_word, fg=current_color)
    window.after(int(reveal_time * 1000), allow_input)

# =====================================================
# FUNCTION: allow_input
# PURPOSE: Enables player input and starts timer
# =====================================================
def allow_input():
    global timer_running
    word_label.config(fg="black")
    entry.config(state='normal')
    entry.focus_set()
    if not timer_running:
        timer_running = True
        countdown()

# =====================================================
# FUNCTION: next_color
# PURPOSE: Checks player's answer and updates score
# =====================================================
def next_color(event=None):
    global score
    if entry['state'] == 'disabled':
        return

    answer = entry.get().strip().lower()
    entry.delete(0, tk.END)

    if answer == current_color.lower():
        score += 1
        score_label.config(text=f"Score: {score}")

    start_round()

# =====================================================
# FUNCTION: end_game
# PURPOSE: Ends the game and saves high score
# =====================================================
def end_game():
    global high_score, timer_running
    entry.config(state='disabled')
    timer_running = False

    if score > high_score:
        high_score = score
        save_high_score()

    word_label.config(
        text=f"Game Over!\nYour Score: {score}\nHigh Score: {high_score}",
        fg="black",
        font=('Helvetica', 20)
    )
    retry_button.pack(pady=10)

# =====================================================
# --- GUI SETUP (OUT OF SYLLABUS) ---
# GUI creation using Tkinter and ttk for visual elements
# =====================================================
window = tk.Tk()
window.title("Color Memory Game")
window.geometry("500x500")

instructions = tk.Label(window, text="Type the COLOR of the word shown (not the word!)",
                        font=('Helvetica', 12))
instructions.pack(pady=10)

score_label = tk.Label(window, text="Score: 0", font=('Helvetica', 12))
score_label.pack()

time_left_label = tk.Label(window, text="Time left: 30", font=('Helvetica', 12))
time_left_label.pack()

timer_bar = ttk.Progressbar(window, length=300, mode='determinate', maximum=30)  # OUT OF SYLLABUS
timer_bar.pack(pady=5)
timer_bar['value'] = 30

word_label = tk.Label(window, font=('Helvetica', 40))
word_label.pack(pady=20)

entry = tk.Entry(window, font=('Helvetica', 14))
entry.pack()
entry.config(state='disabled')

difficulty_var = tk.StringVar()
level_menu = ttk.Combobox(window, textvariable=difficulty_var,
                          values=list(difficulty_levels.keys()),
                          font=('Helvetica', 12), state='readonly')  # OUT OF SYLLABUS
level_menu.set("Select Difficulty")
level_menu.pack(pady=10)

start_button = tk.Button(window, text="Start Game", font=('Helvetica', 16, 'bold'),
                         bg='green', fg='white', padx=20, pady=10, command=on_start_click)
start_button.pack(pady=10)

retry_button = tk.Button(window, text="Play Again", font=('Helvetica', 14, 'bold'),
                         bg='blue', fg='white', padx=15, pady=8, command=retry_game)
retry_button.pack_forget()

window.bind('<Return>', next_color)
window.mainloop()
