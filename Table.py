import tkinter as tk
import numpy as np

class TableApp:
    def __init__(self, root, rows, columns):
        self.root = root
        self.rows = rows
        self.columns = columns
        self.column_headings = [
            "1", "1.4", "2", "2.2", "2.8", "3", "3.2", "3.6", "4", "4.1", 
            "4.2", "4.5", "5", "5.1", "5.4", "5.7", "5.8", "6.0", "6.1-8.0"
        ]
        self.row_headings = [
            "V-C", "V-I", "V-R", "V-G", "I-C", "I-I", "I-R", "I-G", 
            "C-C", "C-I", "C-R", "C-G", "R-C", "R-I", "R-R", "R-G", 
            "A-C", "A-I", "A-R", "A-A"
        ]
        self.table_data = np.zeros((rows, columns), dtype=float)

        self.table_frame = tk.Frame(root)
        self.entry_widgets = []

        for i, row_heading in enumerate(self.row_headings):
            row_label = tk.Label(self.table_frame, text=row_heading, width=5, anchor="w")
            row_label.grid(row=i+1, column=0)
            
            row_entries = []
            for j, col_heading in enumerate(self.column_headings):
                if i == 0:  # Add column headings to the first row
                    col_label = tk.Label(self.table_frame, text=col_heading, width=10)
                    col_label.grid(row=0, column=j+1)
                
                entry = tk.Entry(self.table_frame, width=10)
                entry.grid(row=i+1, column=j+1)
                row_entries.append(entry)
            self.entry_widgets.append(row_entries)

        self.save_button = tk.Button(root, text="Save", command=self.save_data)
        self.save_button.pack()

        self.table_frame.pack()

    def save_data(self):
        for i in range(self.rows):
            for j in range(self.columns):
                entry = self.entry_widgets[i][j]
                value = entry.get()
                try:
                    self.table_data[i, j] = float(value)
                except ValueError:
                    pass

        print("Saved data to NumPy array:\n", self.table_data)


def main():
    rows = 20
    columns = 19

    root = tk.Tk()
    root.title("Editable Table")

    app = TableApp(root, rows, columns)

    root.mainloop()


if __name__ == "__main__":
    main()
