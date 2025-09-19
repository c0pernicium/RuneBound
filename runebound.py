import tkinter as tk

WIDTH, HEIGHT = 800, 500
SIDEBAR_WIDTH = 85
SIDEBAR_PAD = 16
CONTROL_BOX_HEIGHT = 30

PLAYER_SIZE = 32
PLAYER_COLOR = "#FF3333"
PLAYER_SPEED = 7

INVENTORY_SLOTS = 8
INVENTORY_SLOT_SIZE = 50
INVENTORY_SLOT_PAD = 8

# Example base stats
PLAYER_BASE_STATS = {
    "HP": 20,
    "MP": 8,
    "Lvl": 1,
    "XP": 0,

}

class RPGGame:
    def __init__(self, root):
        self.root = root
        self.root.title("RuneBound")
        self.root.configure(bg="#808080")

        # --- Main frame to hold everything horizontally ---
        self.main_frame = tk.Frame(root, bg="#808080")
        self.main_frame.pack(padx=8, pady=(8, 0))

        # --- Left Sidebar (Inventory) ---
        sidebar_height = HEIGHT
        self.left_sidebar = tk.Canvas(
            self.main_frame,
            width=SIDEBAR_WIDTH,
            height=sidebar_height,
            bg="black",
            highlightthickness=4,
            highlightbackground="yellow"
        )
        self.left_sidebar.pack(
            side="left",
            pady=(0, 0),
            padx=(0, SIDEBAR_PAD)
        )

        # --- Game canvas with yellow outline ---
        self.outer_canvas = tk.Frame(self.main_frame, bg='yellow', highlightthickness=0)
        self.outer_canvas.pack(side="left")
        self.canvas = tk.Canvas(
            self.outer_canvas,
            width=WIDTH,
            height=HEIGHT,
            bg="black",
            highlightthickness=4,
            highlightbackground="yellow"
        )
        self.canvas.pack()

        # --- Right Sidebar (Stats) ---
        self.right_sidebar = tk.Canvas(
            self.main_frame,
            width=SIDEBAR_WIDTH,
            height=HEIGHT,
            bg="black",
            highlightthickness=4,
            highlightbackground="yellow"
        )
        self.right_sidebar.pack(
            side="left",
            pady=(0, 0),
            padx=(SIDEBAR_PAD, 0)
        )

        # --- Controls Box (yellow outline, black fill, width = canvas width, half height) ---
        self.controls_frame = tk.Frame(root, bg='yellow', highlightthickness=0, width=WIDTH, height=CONTROL_BOX_HEIGHT+6)
        self.controls_frame.pack(padx=8, pady=(20,8))
        self.controls_inner = tk.Frame(self.controls_frame, bg='black', highlightthickness=0, width=WIDTH, height=CONTROL_BOX_HEIGHT)
        self.controls_inner.pack(padx=3, pady=3, fill="both")
        self.controls_label = tk.Label(
            self.controls_inner,
            text="Controls: W/A/S/D = Move | 1-8 or ↑/↓ = Select Inventory Slot",
            fg="white",
            bg="black",
            font=("Arial", 10),
            anchor="center"
        )
        self.controls_label.pack(fill="both", expand=True)
        self.controls_inner.pack_propagate(False)
        self.controls_inner.config(width=WIDTH, height=CONTROL_BOX_HEIGHT)

        # Player state
        self.player = None
        self.player_x = WIDTH//2 - PLAYER_SIZE//2
        self.player_y = HEIGHT//2 - PLAYER_SIZE//2
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

        # Inventory state (empty)
        self.inventory = [None for _ in range(INVENTORY_SLOTS)]
        self.selected_slot = 0

        # Player stats
        self.stats = PLAYER_BASE_STATS.copy()

        # Key bindings
        self.root.bind('<KeyPress>', self.key_down)
        self.root.bind('<KeyRelease>', self.key_up)

        self.start_game()

    def start_game(self):
        self.canvas.delete("all")
        self.draw_player()
        self.draw_inventory()
        self.draw_stats()
        self.game_loop()

    def draw_player(self):
        if self.player:
            self.canvas.delete(self.player)
        self.player = self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + PLAYER_SIZE, self.player_y + PLAYER_SIZE,
            fill=PLAYER_COLOR, outline="#880000", width=3
        )

    def draw_inventory(self):
        self.left_sidebar.delete("all")
        # Calculate vertical centering for slots
        total_height = INVENTORY_SLOTS * INVENTORY_SLOT_SIZE + (INVENTORY_SLOTS - 1) * INVENTORY_SLOT_PAD
        y_start = (HEIGHT - total_height) // 2

        for i in range(INVENTORY_SLOTS):
            x1 = (SIDEBAR_WIDTH - INVENTORY_SLOT_SIZE) // 2
            y1 = y_start + i * (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_PAD)
            x2 = x1 + INVENTORY_SLOT_SIZE
            y2 = y1 + INVENTORY_SLOT_SIZE
            selected = (i == self.selected_slot)
            # Draw slot background
            self.left_sidebar.create_rectangle(
                x1, y1, x2, y2,
                fill="#222", outline="yellow" if selected else "#666",
                width=4 if selected else 2
            )
            # Draw slot number
            self.left_sidebar.create_text(
                x1 + 13, y1 + 15,
                text=str(i+1),
                fill="#FFF" if selected else "#AAA",
                font=("Arial", 12, "bold")
            )
            # (No item drawing, inventory is empty)

    def draw_stats(self):
        self.right_sidebar.delete("all")
        # Stats box styling
        stat_labels = list(self.stats.keys())
        stat_values = [self.stats[k] for k in stat_labels]
        y_start = 40
        line_height = 32
        label_color = "#F9A825"
        value_color = "#fff"
        title_color = "#4FC3F7"
        # Title
        self.right_sidebar.create_text(
            SIDEBAR_WIDTH//2, 16,
            text="Stats",
            fill=title_color,
            font=("Arial", 14, "bold")
        )
        for i, (label, value) in enumerate(zip(stat_labels, stat_values)):
            y = y_start + i * line_height
            self.right_sidebar.create_text(
                SIDEBAR_WIDTH//2, y,
                text=f"{label}:", fill=label_color,
                font=("Arial", 11, "bold"),
                anchor="e"
            )
            self.right_sidebar.create_text(
                SIDEBAR_WIDTH//2 + 10, y,
                text=f"{value}", fill=value_color,
                font=("Arial", 11, "bold"),
                anchor="w"
            )

    def key_down(self, event):
        key = event.keysym.lower()
        if key == 'w':
            self.move_up = True
        elif key == 's':
            self.move_down = True
        elif key == 'a':
            self.move_left = True
        elif key == 'd':
            self.move_right = True
        elif key in ['up']:
            self.selected_slot = (self.selected_slot - 1) % INVENTORY_SLOTS
            self.draw_inventory()
        elif key in ['down']:
            self.selected_slot = (self.selected_slot + 1) % INVENTORY_SLOTS
            self.draw_inventory()
        elif key in [str(n) for n in range(1, INVENTORY_SLOTS+1)]:
            num = int(key) - 1
            if 0 <= num < INVENTORY_SLOTS:
                self.selected_slot = num
                self.draw_inventory()

    def key_up(self, event):
        key = event.keysym.lower()
        if key == 'w':
            self.move_up = False
        elif key == 's':
            self.move_down = False
        elif key == 'a':
            self.move_left = False
        elif key == 'd':
            self.move_right = False

    def game_loop(self):
        dx = dy = 0
        if self.move_up:
            dy -= PLAYER_SPEED
        if self.move_down:
            dy += PLAYER_SPEED
        if self.move_left:
            dx -= PLAYER_SPEED
        if self.move_right:
            dx += PLAYER_SPEED

        # Move player and clamp to canvas
        if dx or dy:
            new_x = self.player_x + dx
            new_y = self.player_y + dy
            # Clamp
            new_x = max(0, min(WIDTH - PLAYER_SIZE, new_x))
            new_y = max(0, min(HEIGHT - PLAYER_SIZE, new_y))
            self.player_x, self.player_y = new_x, new_y
            self.draw_player()

        self.root.after(16, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = RPGGame(root)
    root.mainloop()
