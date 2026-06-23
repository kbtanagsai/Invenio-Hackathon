import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect("parking.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reservations (
    spot_number INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")
conn.commit()

# --- Functions ---
def load_reservations():
    cursor.execute("SELECT spot_number, name FROM reservations")
    return {row[0]: row[1] for row in cursor.fetchall()}

def update_buttons():
    reservations = load_reservations()
    for spot, btn in buttons.items():
        if spot in reservations:
            btn.config(bg="red", text=f"{spot}\n{reservations[spot]}")
        else:
            btn.config(bg="green", text=f"{spot}\nFree")

def handle_click(spot):
    reservations = load_reservations()
    if spot in reservations:
        # Cancel reservation
        if messagebox.askyesno("Cancel", f"Cancel reservation for spot {spot}?"):
            cursor.execute("DELETE FROM reservations WHERE spot_number=?", (spot,))
            conn.commit()
    else:
        # Reserve spot
        name = simpledialog.askstring("Reserve", f"Enter name for spot {spot}:")
        if name:
            try:
                cursor.execute("INSERT INTO reservations (spot_number, name) VALUES (?, ?)", (spot, name))
                conn.commit()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"Spot {spot} is already reserved!")
    update_buttons()

# --- GUI Setup ---
root = tk.Tk()
root.title("Parking Reservation Grid")

rows = 4   # Number of rows in parking lot
cols = 5   # Number of columns in parking lot
buttons = {}

spot_number = 1
for r in range(rows):
    for c in range(cols):
        btn = tk.Button(root, width=10, height=4, command=lambda s=spot_number: handle_click(s))
        btn.grid(row=r, column=c, padx=5, pady=5)
        buttons[spot_number] = btn
        spot_number += 1

update_buttons()
root.mainloop()

# Close DB on exit
conn.close()
