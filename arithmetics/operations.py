import tkinter as tk
from tkinter import colorchooser, Menu
import argparse

class DigitPaletteApp:

    def __init__(self, root, screen_number):
        self.root = root
        self.screen_number = screen_number
        self.root.title(f"Digit Palette - Screen {self.screen_number}")

        self.palette_frame = tk.Frame(self.root, bg="lightgray", height=50)
        self.palette_frame.pack(fill=tk.X, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.digits = []
        self.lines = []
        self.create_palette()

        self.canvas.bind("<ButtonPress-1>", self.handle_left_click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-3>", self.show_context_menu)

        self.dragged_item = None
        self.context_menu = Menu(self.root, tearoff=0)

        self.drawing_line = False
        self.line_start = None
        self.temp_line = None

        self.drag_start_x = None
        self.drag_start_y = None

        self.symbol_to_drag = None
        self.canvas_item_position = (50, 100)  # Position under the palette where clicked symbol will appear

    def create_palette(self):
        for i in range(10):
            label = tk.Label(self.palette_frame, text=str(i), bg="white", fg="black", width=3, height=1, relief=tk.RAISED)
            label.pack(side=tk.LEFT, padx=2, pady=2)
            label.bind("<Button-1>", self.clone_digit)
        
        for sign in ["+", "=", "-", "\u00D7", "\u00F7"]:
            label = tk.Label(self.palette_frame, text=sign, bg="white", fg="black", width=3, height=1, relief=tk.RAISED)
            label.pack(side=tk.LEFT, padx=2, pady=2)
            label.bind("<Button-1>", self.clone_digit)
            
        # Add letters to the palette
        for letter in ["A", "B", "C", "D", "E", "F", "G", "K", "L", "M", "N"]:
            label = tk.Label(self.palette_frame, text=letter, bg="white", fg="black", width=3, height=1, relief=tk.RAISED)
            label.pack(side=tk.LEFT, padx=2, pady=2)
            label.bind("<Button-1>", self.clone_digit)

        line_mode_button = tk.Button(self.palette_frame, text="Toggle Line Mode", command=self.toggle_line_mode)
        line_mode_button.pack(side=tk.LEFT, padx=5, pady=2)
        
        delete_all_button = tk.Button(self.palette_frame, text="Delete All", command=self.delete_all_drawings)
        delete_all_button.pack(side=tk.LEFT, padx=5, pady=2)

    def delete_all_drawings(self):
        self.canvas.delete("all")
        self.digits.clear()
        self.lines.clear()

    def clone_digit(self, event):
        """Clone the clicked symbol directly under its palette location."""
        label = event.widget
        digit = label["text"]

        # Get the palette symbol's position
        label_x = label.winfo_rootx() - self.root.winfo_rootx()  # Relative to root
        label_y = label.winfo_rooty() - self.root.winfo_rooty()  # Relative to root
        label_width = label.winfo_width()
        label_height = label.winfo_height()

        # Calculate position directly under the clicked symbol
        canvas_x = label_x + label_width // 2
        canvas_y = label_y + label_height + 10  # Add padding below

        # Add the symbol to the canvas
        item = self.canvas.create_text(canvas_x, canvas_y, text=digit, fill="black", font=("Arial", 20), tags="digit")
        self.digits.append(item)

    def handle_left_click(self, event):
        """Handle mouse click on canvas"""
        if not self.drawing_line:
            self.start_drag(event)

    def start_drag(self, event):
        """Start dragging the symbol"""
        item = self.canvas.find_closest(event.x, event.y)
        if "digit" in self.canvas.gettags(item):
            self.dragged_item = item
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def drag(self, event):
        """Move the dragged symbol with the mouse"""
        if self.dragged_item:
            if self.drag_start_x is not None and self.drag_start_y is not None:
                delta_x = event.x - self.drag_start_x
                delta_y = event.y - self.drag_start_y
                self.canvas.move(self.dragged_item, delta_x, delta_y)
                self.drag_start_x = event.x
                self.drag_start_y = event.y

    def end_drag(self, event):
        """End the drag and drop"""
        self.dragged_item = None
        self.drag_start_x = None
        self.drag_start_y = None

    def show_context_menu(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(item)

        self.context_menu.delete(0, tk.END)

        if "digit" in tags:
            self.context_menu.add_command(label="Change Color", command=lambda: self.change_color(item))
            self.context_menu.add_command(label="Delete", command=lambda: self.delete_item(item))
        elif "line" in tags:
            self.context_menu.add_command(label="Delete", command=lambda: self.delete_item(item))

        self.context_menu.post(event.x_root, event.y_root)

    def change_color(self, item):
        color = colorchooser.askcolor()[1]
        if color:
            self.canvas.itemconfig(item, fill=color)

    def delete_item(self, item):
        self.canvas.delete(item)
        if item in self.digits:
            self.digits.remove(item)
        elif item in self.lines:
            self.lines.remove(item)

    def toggle_line_mode(self):
        self.drawing_line = not self.drawing_line
        mode = "Line Drawing" if self.drawing_line else "Dragging"
        self.root.title(f"Digit Palette - Screen {self.screen_number} - {mode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digit Palette App")
    parser.add_argument("screen_number", type=int, help="Screen number to display in the title")
    args = parser.parse_args()

    root = tk.Tk()
    app = DigitPaletteApp(root, args.screen_number)
    root.mainloop()