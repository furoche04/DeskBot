import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from core.file_organizer import organize_downloads, organize_desktop, FileOrganizer
from pathlib import Path

class OrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Smart Organizer")
        self.root.geometry("650x500")

        # Buttons
        button_frame = ttk.Frame(root, padding="10")
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Organize Downloads", command=self.run_downloads).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Organize Desktop", command=self.run_desktop).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Choose Directory...", command=self.choose_and_run).pack(side="left", padx=5)

        # Log area
        log_frame = ttk.LabelFrame(root, text="Logs", padding="10")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=18, state="disabled")
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

    def choose_and_run(self):
        dir_path = filedialog.askdirectory(title="Select a directory to organize")
        if not dir_path:
            return
        organizer = FileOrganizer()
        directory = Path(dir_path)
        if directory.exists():
            files = [f for f in directory.iterdir() if f.is_file()]
            stats = organizer.organize_files(files)
            self.log(f"Custom directory '{directory}' organized: {stats}")
        else:
            self.log(f"Directory not found: {directory}")


def run_gui():
    root = tk.Tk()
    app = OrganizerGUI(root)
    root.mainloop()
