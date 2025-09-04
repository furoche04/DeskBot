import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from pathlib import Path
from datetime import datetime
import csv

from core.file_organizer import FileOrganizer
from core.system_monitor import SystemMonitor
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
        self.update_system_stats()  # Start monitoring

    def create_widgets(self):
        # ---------- File Organizer Frame ----------
        organizer_frame = ttk.LabelFrame(self.root, text="File Organizer")
        organizer_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(organizer_frame, text="Organize Downloads", command=self.organize_downloads).pack(side="left", padx=5, pady=5)
        ttk.Button(organizer_frame, text="Organize Desktop", command=self.organize_desktop).pack(side="left", padx=5, pady=5)
        ttk.Button(organizer_frame, text="Custom Directory", command=self.organize_custom_directory).pack(side="left", padx=5, pady=5)

        ttk.Button(organizer_frame, text="Export Logs & Usage to CSV", command=self.export_logs).pack(side="right", padx=5, pady=5)

        # ---------- Live Action Log Frame ----------
        log_frame = ttk.LabelFrame(self.root, text="Live Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_area = scrolledtext.ScrolledText(log_frame, state="disabled", height=15)
        self.log_area.pack(fill="both", expand=True)

        # ---------- System Monitor Frame ----------
        monitor_frame = ttk.LabelFrame(self.root, text="System Usage")
        monitor_frame.pack(fill="x", padx=10, pady=5)

        self.labels = {}
        for metric in ["CPU", "Memory", "Disk"]:
            frame = ttk.Frame(monitor_frame)
            frame.pack(fill="x", pady=2)
            label = ttk.Label(frame, text=f"{metric}: 0%")
            label.pack(side="left", padx=5)
            self.labels[metric.lower()] = label

    # ---------- File Organizer Functions ----------
    def organize_downloads(self):
        stats = self.file_organizer.organize_files()
        message = f"Organized Downloads: {stats}"
        self.append_action_log("Downloads", stats, message)

    def organize_desktop(self):
        desktop_path = [Path.home() / "Desktop"]
        files = self.file_organizer.scan_directories_from_list(desktop_path)
        stats = self.file_organizer.organize_files(files)
        message = f"Organized Desktop: {stats}"
        self.append_action_log("Desktop", stats, message)

    def organize_custom_directory(self):
        folder = filedialog.askdirectory(title="Select Custom Directory")
        if not folder:
            self.append_log("No directory selected for custom organization.")
            return
        folder_path = [Path(folder)]
        files = self.file_organizer.scan_directories_from_list(folder_path)
        stats = self.file_organizer.organize_files(files)
        message = f"Organized Custom Directory ({folder}): {stats}"
        self.append_action_log("Custom", stats, message)

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

    # ---------- System Monitor Functions ----------
    def update_system_stats(self):
        stats = self.monitor.get_stats()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update labels
        self.labels["cpu"].config(text=f"CPU: {stats['cpu_percent']}%")
        self.labels["memory"].config(text=f"Memory: {stats['memory_percent']}%")
        self.labels["disk"].config(text=f"Disk: {stats['disk_percent']}%")

        # Append to session log only (for CSV export)
        self.session_logs.append({
            "timestamp": timestamp,
            "type": "system",
            "cpu": stats['cpu_percent'],
            "memory": stats['memory_percent'],
            "disk": stats['disk_percent'],
            "event": ""
        })

        # Refresh every 5 seconds
        self.root.after(5000, self.update_system_stats)

    # ---------- Logging ----------
    def append_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    # ---------- Export to CSV ----------
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
