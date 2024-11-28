import tkinter as tk
from tkinter import filedialog, messagebox

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genetic Quine-McCluskey")
        self.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Select Testcase File: ")
        self.label.pack(pady=10)

        self.file_entry = tk.Entry(self, width=50)
        self.file_entry.pack(pady=5)

        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.run_button = tk.Button(self, text="Run Algorithm", command=self.run_algorithm)
        self.run_button.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
    
    def run_algorithm(self):
        messagebox.showinfo("Algorithm", "Algorithm is running...")