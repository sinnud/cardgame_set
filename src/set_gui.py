import tkinter as tk
from tkinter import messagebox
import random
from core import SetGame

CARD_ROWS = 3
CARD_COLS = 8
BASE_COLS = 4
VISIBLE_CARDS = 12
EXTRA_CARDS_PER_GIVEUP = 3
MAX_GIVEUPS = 3
MAX_VISIBLE_CARDS = VISIBLE_CARDS + (EXTRA_CARDS_PER_GIVEUP * MAX_GIVEUPS)

# Calculated thresholds
COL4_START = VISIBLE_CARDS
COL5_START = COL4_START + EXTRA_CARDS_PER_GIVEUP
COL6_START = COL5_START + EXTRA_CARDS_PER_GIVEUP

class SetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SET Card Game")
        self.selected_indices = []
        self.card_buttons = []
        self.freeze = False
        self.game = SetGame()
        self.cards = self.game.deal_initial_cards()
        self.visible_count = VISIBLE_CARDS
        self.give_up_count = 0
        self.max_give_ups = 3
        self.played_count = 0

        self.create_desk()
        self.create_controls()

    def create_desk(self):
        desk_frame = tk.Frame(self.root)
        desk_frame.pack(padx=10, pady=(10, 5))

        for r in range(CARD_ROWS):
            for c in range(CARD_COLS):
                idx = r * CARD_COLS + c
                btn = tk.Canvas(
                    desk_frame,
                    width=120, height=160,
                    relief=tk.RAISED,
                    bg='white'
                )
                
                if c < 4:
                    card_idx = r * 4 + c
                    if card_idx < self.visible_count:
                        self.draw_card_on_canvas(btn, self.cards[card_idx])
                        btn.bind('<Button-1>', lambda e, card_i=card_idx: self.toggle_select(card_i))
                elif c == 4:
                    extra_idx = 12 + r
                    if extra_idx < self.visible_count:
                        self.draw_card_on_canvas(btn, self.cards[extra_idx])
                        btn.bind('<Button-1>', lambda e, extra_i=extra_idx: self.toggle_select(extra_i))
                    else:
                        btn.config(bg='white')
                elif c == 5:
                    extra_idx = 15 + r
                    if extra_idx < self.visible_count:
                        self.draw_card_on_canvas(btn, self.cards[extra_idx])
                        btn.bind('<Button-1>', lambda e, extra_i=extra_idx: self.toggle_select(extra_i))
                    else:
                        btn.config(bg='white')
                elif c == 6:
                    extra_idx = 18 + r
                    if extra_idx < self.visible_count:
                        self.draw_card_on_canvas(btn, self.cards[extra_idx])
                        btn.bind('<Button-1>', lambda e, extra_i=extra_idx: self.toggle_select(extra_i))
                    else:
                        btn.config(bg='white')
                elif c == 7 and r < 3:
                    btn.config(bg='lightgray')
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.card_buttons.append(btn)

    def toggle_select(self, idx):
        if self.freeze or idx >= self.visible_count:
            return

        if idx < VISIBLE_CARDS:
            row = idx // BASE_COLS
            col = idx % BASE_COLS
            btn_idx = row * CARD_COLS + col
        elif idx < COL5_START:
            row = idx - COL4_START
            col = 4
            btn_idx = row * CARD_COLS + col
        elif idx < COL6_START:
            row = idx - COL5_START
            col = 5
            btn_idx = row * CARD_COLS + col
        else:
            row = idx - COL6_START
            col = 6
            btn_idx = row * CARD_COLS + col
        
        btn = self.card_buttons[btn_idx]
        if idx in self.selected_indices:
            self.selected_indices.remove(idx)
            btn.config(bg="white")
            self.draw_card_on_canvas(btn, self.cards[idx])
            self.clear_selected_display()
        else:
            if len(self.selected_indices) < 3:
                self.selected_indices.append(idx)
                btn.config(bg="lightblue")
            if len(self.selected_indices) == 3:
                self.update_selected_display()
                self.root.update()
                self.freeze = True
                self.show_popup()

    
    def draw_card_on_canvas(self, canvas, card):
        canvas.delete('all')
        color = card['color']
        shape = card['shape']
        number = card['number']
        shading = card['shading']
        
        shape_height = 40
        y_spacing = 50
        
        if number == 1:
            y_start = 60
        elif number == 2:
            y_start = 35
        else:
            y_start = 20
        
        for i in range(number):
            y = y_start + i * y_spacing
            
            if shape == '○':
                if shading == 'filled':
                    canvas.create_oval(40, y, 80, y+shape_height, fill=color, outline=color, width=2)
                elif shading == 'striped':
                    canvas.create_oval(40, y, 80, y+shape_height, fill='white', outline=color, width=2)
                    for stripe in range(8):
                        canvas.create_line(45+stripe*4, y+5, 45+stripe*4, y+shape_height-5, fill=color, width=1)
                else:
                    canvas.create_oval(40, y, 80, y+shape_height, fill='white', outline=color, width=2)
            elif shape == '△':
                points = [60, y+5, 45, y+shape_height-5, 75, y+shape_height-5]
                if shading == 'filled':
                    canvas.create_polygon(points, fill=color, outline=color, width=2)
                elif shading == 'striped':
                    canvas.create_polygon(points, fill='white', outline=color, width=2)
                    for stripe in range(6):
                        y_stripe = y + 10 + stripe * 5
                        x_left = 52 - stripe * 2
                        x_right = 68 + stripe * 2
                        if x_left < x_right:
                            canvas.create_line(x_left, y_stripe, x_right, y_stripe, fill=color, width=1)
                else:
                    canvas.create_polygon(points, fill='white', outline=color, width=2)
            elif shape == '□':
                if shading == 'filled':
                    canvas.create_rectangle(45, y+5, 75, y+shape_height-5, fill=color, outline=color, width=2)
                elif shading == 'striped':
                    canvas.create_rectangle(45, y+5, 75, y+shape_height-5, fill='white', outline=color, width=2)
                    for stripe in range(7):
                        canvas.create_line(50+stripe*4, y+8, 50+stripe*4, y+shape_height-8, fill=color, width=1)
                else:
                    canvas.create_rectangle(45, y+5, 75, y+shape_height-5, fill='white', outline=color, width=2)
    
    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)
        
        help_btn = tk.Button(control_frame, text="Help", command=self.show_help, width=10)
        help_btn.pack(side=tk.LEFT, padx=5)
        
        self.give_up_btn = tk.Button(control_frame, text=f"Give Up ({self.max_give_ups - self.give_up_count} left)", 
                                    command=self.give_up, width=15)
        self.give_up_btn.pack(side=tk.LEFT, padx=5)
        
        self.score_label = tk.Label(control_frame, text=f"Score: {self.game.score}", width=10)
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        self.count_label = tk.Label(control_frame, text=f"Played: {self.played_count}", width=10)
        self.count_label.pack(side=tk.LEFT, padx=5)
    
    def show_help(self):
        help_text = """SET Card Game Rules:

Operation Manual:
• Click cards to select them (up to 3)
• Click selected cards to unselect them
• After selecting 3 cards, they move to the right column
• A popup shows if you found a valid SET or not

SET Rules:
A SET is 3 cards where each property is either:
- ALL THE SAME across the 3 cards, OR
- ALL DIFFERENT across the 3 cards

Properties:
• Shape: Circle (○), Triangle (△), Square (□)
• Color: Red, Green, Blue
• Number: 1, 2, or 3 shapes
• Shading: Outline, Striped, Filled

Examples:
✓ VALID SET: All same color, all different shapes, all same number
✓ VALID SET: All different colors, all same shape, all different numbers
✗ INVALID: 2 red cards + 1 blue card (not all same, not all different)

Scoring: +1 for correct SET, -1 for incorrect guess"""
        
        messagebox.showinfo("Help - SET Rules", help_text)
    
    def give_up(self):
        if self.give_up_count >= self.max_give_ups or self.freeze:
            return
        
        extra_cards = self.game.get_replacement_cards(3)
        if not extra_cards:
            messagebox.showinfo("No More Cards", "No more cards available in deck!")
            return
            
        column = 4 + self.give_up_count
        
        for i, card in enumerate(extra_cards):
            if self.visible_count < MAX_VISIBLE_CARDS:
                card_idx = self.visible_count
                self.cards.append(card)
                canvas_idx = i * CARD_COLS + column
                canvas = self.card_buttons[canvas_idx]
                canvas.config(bg='white')
                self.draw_card_on_canvas(canvas, card)
                canvas.bind('<Button-1>', lambda e, idx=card_idx: self.toggle_select(idx))
                self.visible_count += 1
        
        self.give_up_count += 1
        self.give_up_btn.config(text=f"Give Up ({self.max_give_ups - self.give_up_count} left)")
        if self.give_up_count >= self.max_give_ups:
            self.give_up_btn.config(state=tk.DISABLED)
    
    def get_canvas_for_card_index(self, idx):
        if idx < VISIBLE_CARDS:
            row = idx // BASE_COLS
            col = idx % BASE_COLS
            btn_idx = row * CARD_COLS + col
        elif idx < COL5_START:
            row = idx - COL4_START
            col = 4
            btn_idx = row * CARD_COLS + col
        elif idx < COL6_START:
            row = idx - COL5_START
            col = 5
            btn_idx = row * CARD_COLS + col
        else:
            row = idx - COL6_START
            col = 6
            btn_idx = row * CARD_COLS + col
        return self.card_buttons[btn_idx]
    
    def clear_selected_display(self):
        for i in range(3):
            right_canvas = self.card_buttons[i * CARD_COLS + 7]
            right_canvas.delete('all')
            right_canvas.config(bg='lightgray')
        
        for idx in self.selected_indices:
            original_canvas = self.get_canvas_for_card_index(idx)
            original_canvas.config(bg='white')
            self.draw_card_on_canvas(original_canvas, self.cards[idx])

    def update_selected_display(self):
        for i, selected_idx in enumerate(self.selected_indices):
            if i < 3:
                selected_card = self.cards[selected_idx]
                right_col_canvas = self.card_buttons[i * CARD_COLS + 7]
                self.draw_card_on_canvas(right_col_canvas, selected_card)
                
                original_canvas = self.get_canvas_for_card_index(selected_idx)
                original_canvas.delete('all')
                original_canvas.config(bg='lightgray')
    
    def show_popup(self):
        selected_cards = [self.cards[i] for i in self.selected_indices]
        is_set, result_msg = self.game.process_selection(selected_cards)
        
        self.played_count += 1
        self.update_score_display()
        
        result = messagebox.askyesno("Game Result", f"{result_msg}\n\nContinue playing?", icon='question')
        
        if result:
            self.continue_game()
        else:
            self.root.quit()
    
    def update_score_display(self):
        self.score_label.config(text=f"Score: {self.game.score}")
        self.count_label.config(text=f"Played: {self.played_count}")
    
    def show_game_over(self):
        final_msg = f"Game Over!\n\nFinal Score: {self.game.score}\nRounds Played: {self.played_count}\n\nNo more cards available."
        messagebox.showinfo("Game Over", final_msg)
        self.root.quit()
    
    def continue_game(self):
        self.clear_selected_display()
        
        # Remove selected cards
        selected_sorted = sorted(self.selected_indices, reverse=True)
        for idx in selected_sorted:
            del self.cards[idx]
        
        # Only add replacement cards if we have less than 12 cards remaining
        if len(self.cards) < 12:
            needed_cards = 12 - len(self.cards)
            replacement_cards = self.game.get_replacement_cards(needed_cards)
            if replacement_cards:
                self.cards.extend(replacement_cards)
            elif self.game.is_deck_exhausted() and len(self.cards) < 3:
                self.show_game_over()
        
        self.visible_count = len(self.cards)
        
        # Reorder cards to fill left columns first
        self.reorder_and_redraw_cards()
        
        self.selected_indices = []
        self.freeze = False
    
    def reorder_and_redraw_cards(self):
        # Clear all canvases
        for canvas in self.card_buttons:
            canvas.delete('all')
            canvas.config(bg='white')
        
        # Redraw cards in order: first 12 in left 4 columns, then extras in columns 4,5,6
        for i, card in enumerate(self.cards):
            if i < 12:
                # First 12 cards go in left 4 columns
                row = i // 4
                col = i % 4
                canvas_idx = row * CARD_COLS + col
            elif i < 15:
                # Next 3 cards go in column 4
                row = i - 12
                col = 4
                canvas_idx = row * CARD_COLS + col
            elif i < 18:
                # Next 3 cards go in column 5
                row = i - 15
                col = 5
                canvas_idx = row * CARD_COLS + col
            else:
                # Next 3 cards go in column 6
                row = i - 18
                col = 6
                canvas_idx = row * CARD_COLS + col
            
            canvas = self.card_buttons[canvas_idx]
            canvas.config(bg='white')
            self.draw_card_on_canvas(canvas, card)
            canvas.bind('<Button-1>', lambda e, card_i=i: self.toggle_select(card_i))
        # You can process the selected cards here

if __name__ == "__main__":
    root = tk.Tk()
    app = SetGUI(root)
    root.mainloop()