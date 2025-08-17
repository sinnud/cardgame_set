import tkinter as tk
from tkinter import messagebox

CARD_ROWS = 3
CARD_COLS = 8
TOTAL_CARDS = 24
VISIBLE_CARDS = 12

class SetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SET Card Game")
        self.selected_indices = []
        self.card_buttons = []
        self.freeze = False

        self.create_desk()

    def create_desk(self):
        desk_frame = tk.Frame(self.root)
        desk_frame.pack(padx=10, pady=10)

        for r in range(CARD_ROWS):
            for c in range(CARD_COLS):
                idx = r * CARD_COLS + c
                btn = tk.Button(
                    desk_frame,
                    text=f"Card {idx+1}" if idx < VISIBLE_CARDS else "",
                    width=12, height=4,
                    relief=tk.RAISED,
                    state=tk.NORMAL if idx < VISIBLE_CARDS else tk.DISABLED,
                    command=lambda i=idx: self.toggle_select(i)
                )
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.card_buttons.append(btn)

    def toggle_select(self, idx):
        if self.freeze or idx >= VISIBLE_CARDS:
            return

        btn = self.card_buttons[idx]
        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
            btn.config(bg="SystemButtonFace")
        else:
            if len(self.selected_indices) < 3:
                self.selected_indices.append(idx)
                btn.config(bg="lightblue")
            if len(self.selected_indices) == 3:
                self.freeze = True
                self.show_selected_cards()

    def show_selected_cards(self):
        selected = [f"Card {i+1}" for i in self.selected_indices]
        messagebox.showinfo("Selected Cards", f"You selected: {', '.join(selected)}")
        # You can process the selected cards here

if __name__ == "__main__":
    root = tk.Tk()
    app = SetGUI(root)