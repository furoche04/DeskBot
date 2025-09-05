import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path
from datetime import datetime
import threading
import csv

from core.file_organizer import FileOrganizer
from core.system_monitor import SystemMonitor
from core.ocr_processor import ocr_processor
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DeskBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DeskBot - Desktop Smart Organizer")
        self.root.geometry("600x500")

        self.monitor = SystemMonitor()
        self.file_organizer = FileOrganizer()
        self.session_logs = []

        self.create_widgets()
        self.update_system_stats()  # Start system monitoring

    # ---------------- GUI Setup ----------------
    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)

        # Organizer Tab
        organizer_tab = ttk.Frame(notebook)
        notebook.add(organizer_tab, text="Organizer")
        self.create_organizer_tab(organizer_tab)

        # Logs Tab
        logs_tab = ttk.Frame(notebook)
        notebook.add(logs_tab, text="Logs")
        self.create_logs_tab(logs_tab)

        # OCR Tab
        ocr_tab = ttk.Frame(notebook)
        notebook.add(ocr_tab, text="OCR")
        self.create_ocr_tab(ocr_tab)

        # System Tab
        system_tab = ttk.Frame(notebook)
        notebook.add(system_tab, text="System")
        self.create_system_tab(system_tab)

    # ---------------- Organizer ----------------
    def create_organizer_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="File Organizer")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(frame, text="Organize Downloads", command=self.organize_downloads).pack(side="left", padx=5, pady=5)
        ttk.Button(frame, text="Organize Desktop", command=self.organize_desktop).pack(side="left", padx=5, pady=5)
        ttk.Button(frame, text="Custom Directory", command=self.organize_custom_directory).pack(side="left", padx=5, pady=5)
        ttk.Button(frame, text="Export Logs & Usage to CSV", command=self.export_logs).pack(side="right", padx=5, pady=5)

    # ---------------- Logs ----------------
    def create_logs_tab(self, parent):
        log_frame = ttk.LabelFrame(parent, text="Live Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, state="disabled", height=20)
        self.log_area.pack(fill="both", expand=True)

    # ---------------- OCR ----------------
    def create_ocr_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="Screenshot & OCR")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Take Screenshot & OCR", command=self.run_ocr).pack(pady=10)

        self.ocr_output = scrolledtext.ScrolledText(frame, state="disabled", height=15)
        self.ocr_output.pack(fill="both", expand=True)

    def run_ocr(self):
        """Run OCR in a separate thread to avoid blocking GUI"""
        threading.Thread(target=self._ocr_thread, daemon=True).start()

    def _ocr_thread(self):
        try:
            text_file, text = ocr_processor.screenshot_and_ocr()

            # Update logs
            self.append_log(f"OCR run: saved to {text_file}")
            self.session_logs.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "ocr",
                "cpu": None,
                "memory": None,
                "disk": None,
                "event": f"OCR saved to {text_file}"
            })

            # Update OCR output in main thread
            self.root.after(0, lambda: self._update_ocr_output(text))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("OCR Error", str(e)))

    def _update_ocr_output(self, text):
        self.ocr_output.configure(state="normal")
        self.ocr_output.delete("1.0", "end")
        self.ocr_output.insert("end", text)
        self.ocr_output.configure(state="disabled")

    # ---------------- System ----------------
    def create_system_tab(self, parent):
        frame = ttk.LabelFrame(parent, text="System Usage")
        frame.pack(fill="x", padx=10, pady=5)

        self.labels = {}
        for metric in ["CPU", "Memory", "Disk"]:
            row = ttk.Frame(frame)
            row.pack(fill="x", pady=2)
            label = ttk.Label(row, text=f"{metric}: 0%")
            label.pack(side="left", padx=5)
            self.labels[metric.lower()] = label

    # ---------------- File Organizer ----------------
    def organize_downloads(self):
        try:
            stats = self.file_organizer.organize_files()
            message = f"Organized Downloads: {stats}"
            self.append_action_log("Downloads", stats, message)
        except Exception as e:
            self.append_log(f"Error organizing Downloads: {e}")

    def organize_desktop(self):
        try:
            desktop_path = [Path.home() / "Desktop"]
            files = self.file_organizer.scan_directories_from_list(desktop_path)
            stats = self.file_organizer.organize_files(files)
            message = f"Organized Desktop: {stats}"
            self.append_action_log("Desktop", stats, message)
        except Exception as e:
            self.append_log(f"Error organizing Desktop: {e}")

    def organize_custom_directory(self):
        folder = filedialog.askdirectory(title="Select Custom Directory")
        if not folder:
            self.append_log("No directory selected for custom organization.")
            return
        try:
            folder_path = [Path(folder)]
            files = self.file_organizer.scan_directories_from_list(folder_path)
            stats = self.file_organizer.organize_files(files)
            message = f"Organized Custom Directory ({folder}): {stats}"
            self.append_action_log("Custom", stats, message)
        except Exception as e:
            self.append_log(f"Error organizing custom directory: {e}")

    def append_action_log(self, directory_type, stats, message):
        logger.info(message)
        self.append_log(message)
        self.session_logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "organizer",
            "cpu": None,
            "memory": None,
            "disk": None,
            "event": message
        })

    # ---------------- System Monitor ----------------
    def update_system_stats(self):
        stats = self.monitor.get_stats()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.labels["cpu"].config(text=f"CPU: {stats['cpu_percent']}%")
        self.labels["memory"].config(text=f"Memory: {stats['memory_percent']}%")
        self.labels["disk"].config(text=f"Disk: {stats['disk_percent']}%")

        self.session_logs.append({
            "timestamp": timestamp,
            "type": "system",
            "cpu": stats['cpu_percent'],
            "memory": stats['memory_percent'],
            "disk": stats['disk_percent'],
            "event": ""
        })

        self.root.after(5000, self.update_system_stats)

    # ---------------- Logging ----------------
    def append_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    # ---------------- Export ----------------
    def export_logs(self):
        if not self.session_logs:
            self.append_log("No session logs to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Session Logs"
        )
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["timestamp", "type", "cpu", "memory", "disk", "event"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for entry in self.session_logs:
                    writer.writerow(entry)
            self.append_log(f"Session logs exported to {file_path}")
        except Exception as e:
            self.append_log(f"Failed to export logs: {e}")


def run_gui():
    root = tk.Tk()
    app = DeskBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
