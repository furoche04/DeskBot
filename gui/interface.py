import tkinter as tk
from tkinter import ttk, scrolledtext
from core.file_organizer import organize_downloads, organize_desktop

class OrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Smart Organizer")
        self.root.geometry("600x400")

        # Buttons
        button_frame = ttk.Frame(root, padding="10")
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Organize Downloads", command=self.run_downloads).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Organize Desktop", command=self.run_desktop).pack(side="left", padx=5)

        # Log area
        log_frame = ttk.LabelFrame(root, text="Logs", padding="10")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15, state="disabled")
        self.log_area.pack(fill="both", expand=True)

    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def run_downloads(self):
        stats = organize_downloads()
        self.log(f"Downloads organized: {stats}")

    def run_desktop(self):
        stats = organize_desktop()
        self.log(f"Desktop organized: {stats}")


def run_gui():
    root = tk.Tk()
    app = OrganizerGUI(root)
    root.mainloop()

