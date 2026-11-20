"""
SnakeGH - A Classic Arcade Game
Lab 2 - Python (Level 200)
Name: Adjei Dodo-Mensah Alexander | 2526405108
"""

import random
import tkinter as tk

CELL = 24
COLS = 25
ROWS = 20
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL
START_SPEED = 150
HIGH_SCORE_FILE = "snake_highscore.txt"
DIRECTIONS = {"Up": (0, -1), "Down": (0, 1), "Right": (1, 0), "Left": (-1, 0)}
OPPOSITE = {"Up": "Down", "Down": "Up", "Right": "Left", "Left": "Right"}
KEYS = { "up": "Up", "w": "Up","down": "Down", "s": "Down",
         "left": "Left", "a": "Left", "right": "Right", "d": "Right"}

# ------------ Logic functions ----------------
# ------------ Game State -------------

snake = []
direction = "Right"
next_direction = "Right"
food = (0, 0)
score = 0
level = 1
high_score = "load_high_score()"
running = False
paused = False
loop_id = None


# ------------ GUI event handlers ----------------

def draw_grid():
    """Draw the grid lines once, at the start of the game."""
    for x in range(0, WIDTH, CELL):
        canvas.create_line(x, 0, x, HEIGHT, fill="black")
    for y in range(0, HEIGHT, CELL):
        canvas.create_line(0, y, WIDTH, y, fill="black")


def update_labels():
    score_label.config(text=f"Score: {score}  Level: {level}   Best: {high_score}")


def draw_eyes(x, y):
    """Two small white ovals on the head, pushed toward the direction of travel."""
    dx, dy = DIRECTIONS[direction]
    cx = x * CELL + CELL // 2
    cy = y * CELL + CELL // 2
    rx = 4 if dx else 3   # make each oval slightly longer along the travel axis
    ry = 4 if dy else 3
    for side in (-1, 1):
        ex = cx + dx * 5 + (-dy) * side * 5
        ey = cy + dy * 5 + dx * side * 5
        canvas.create_oval(ex - rx, ey - ry, ex + rx, ey + ry,
                           fill="white", outline="", tags="piece")

def draw():
    """Clear the old snake and food, then draw them in their new places."""
    canvas.delete("piece", "message")
    fx, fy = food
    canvas.create_oval(fx * CELL + 4, fy * CELL + 4, fx * CELL + CELL - 4, fy * CELL + CELL - 4,
                       fill="#e53935", outline="", tags="piece")
    for index, (x, y) in enumerate(snake):
        colour = "navy" if index == 0 else "dodger blue"
        canvas.create_rectangle(x * CELL + 1, y * CELL + 1, x * CELL + CELL - 1, y * CELL + CELL - 1,
                                fill=colour, outline="", tags="piece")
        if index == 0:
            draw_eyes(x, y)
    update_labels()


def show_message(title, subtitle):
    """Write a big message in the middle of the board."""
    canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text=title,
fill="white",
                       font=("Segoe UI", 28, "bold"), tags="message")
    canvas.create_text(WIDTH // 2, HEIGHT // 2 + 20, text=subtitle,
fill="#bbbbbb",
                       font=("Segoe UI", 12), tags="message")

def start_game(event=None):
    global snake, direction, next_direction, food, score, level, running,\
paused, loop_id
    if loop_id is not None:
        root.after_cancel(loop_id)
    snake = [(5, 10), (4, 10), (3, 10)]
    direction = "Right"
    next_direction = "Right"
    food = random_food(snake)
    score = 0
    level = 1
    running = True
    paused = False
    draw()
    loop_id = root.after(speed_for(level), game_loop)


def game_loop():
    """One tick: move, draw, then schedule the next tick."""
    global direction, food, score, level, loop_id
    direction = next_direction
    head = next_head(snake[0], direction)
    if hits_wall(head) or hit_self(head, snake):
        game_over()
        return


    snake.insert(0, head)
    if head == food:
        score += 1
        level = level_for(score)
        food = random_food(snake)
    else:
        snake.pop()

    draw()
    loop_id = root.after(speed_for(level), game_loop)


def on_key(event):
    """Change direction, but never straight back into the body."""
    global next_direction
    new_direction = KEYS.get(event.keysym.lower())
    if new_direction is None or not running or paused:
        return
    if new_direction != OPPOSITE[direction]:
            next_direction = new_direction


def on_enter(event=None):
    if not running:
        start_game()


def toggle_pause(event=None):
    global paused, loop_id
    if not running:
        return
    paused = not paused
    if paused:
        root.after_cancel(loop_id)
        show_message("PAUSED", "Press Space to continue")
    else:
        canvas.delete("message")
        loop_id = root.after(speed_for(level), game_loop)


def game_over():
    global running, high_score
    running = False
    if score > high_score:
        high_score = score
        save_high_score(high_score)
        show_message("NEW HIGH SCORE!", f"You scored {score}. Press Enter to play again")
    else:
        show_message("GAME OVER", f"You scored {score}. Press Enter to play again")
    update_labels()


# --------------- BUiLD THE WINDOW -------------

root = tk.Tk()
root.title("SnakeGH - Classic Arcade Game")
root.resizable(width=False, height=False)
root.config(bg="white")

tk.Label(root, text="SnakeGH", font=("Segoe UI", 22, "bold"),
         fg="green").pack(pady=(10,0))

score_label = tk.Label(root, text="Score: 0    Level: 1   Best:0", font=
("Consolas", 13, "bold"), fg="black")
score_label.pack(pady=(0,8))

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#121212",
highlightthickness=0)
canvas.pack(padx=15)

tk.Label(root, text="Arrows / W A S D = move   Space = pause   Enter = start",
         fg="green", bg="white").pack(pady=8)

def next_head(head, direction):
    """Return the square the head moves into."""
    dx, dy = DIRECTIONS[direction]
    x, y = head
    return x + dx, y + dy


def hits_wall(cell):
    """True if the square is outside the board"""
    x, y = cell
    return x < 0 or x>= COLS or y < 0 or y >= ROWS


def hit_self(head, snake):
    """True if the head runs into the body"""
    return head in snake[:-1]


def random_food(snake):
    """Generate a random food cell"""
    free = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in snake]
    return random.choice(free)


def level_for(score):
    """Level goes up every 5 points."""
    return score // 5 + 1


def speed_for(score):
    """Speed goes up every 5 points."""
    return max(60, START_SPEED - (level - 1) * 15)


def load_high_score():
    """Read the high score file, 0 if there is no high score."""
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    """Save the new high score file."""
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))

high_score = load_high_score()

root.bind("<Key>", on_key)
root.bind("<Return>", on_enter)
root.bind("<space>", toggle_pause)

draw_grid()
update_labels()
show_message("SnakeGH", "Press Enter to start")


root.mainloop()