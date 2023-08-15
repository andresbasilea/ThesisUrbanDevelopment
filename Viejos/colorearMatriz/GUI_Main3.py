import tkinter as tk

class ColorGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Grid")

        self.canvas = tk.Canvas(root, width=500, height=500, bg='white')
        self.canvas.pack()

        self.colors = ["red", "blue", "green", "yellow", "purple"]
        self.selected_color = self.colors[0]

        self.create_grid()
        self.create_color_buttons()

        self.canvas.bind("<Button-1>", self.color_cell)

    def create_grid(self):
        cell_size = 10
        for row in range(50):
            for col in range(50):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')

    def create_color_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        for color in self.colors:
            color_button = tk.Button(button_frame, bg=color, width=3, command=lambda c=color: self.select_color(c))
            color_button.pack(side='left', padx=5, pady=5)

    def select_color(self, color):
        self.selected_color = color

    def color_cell(self, event):
        cell_size = 10
        col = event.x // cell_size
        row = event.y // cell_size
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline='black')

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorGridApp(root)
    root.mainloop()
