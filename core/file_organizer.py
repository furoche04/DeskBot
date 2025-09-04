import os
from pathlib import Path
import shutil
import logging
import time
from datetime import datetime

class Settings:
    FILE_CATEGORIES = {
        '.txt': 'Text',
        '.jpg': 'Images',
        '.png': 'Images',
        '.pdf': 'Documents',
    }
    ORGANIZED_FILES_DIR = Path.home() / "Organized"
    BACKUP_BEFORE_MOVE = True

settings = Settings()
logger = logging.getLogger(__name__)

class FileOrganizer:
    def __init__(self):
        self.organized_count = 0
        self.error_count = 0
        self.last_run = None

    # previous methods: scan_directories, categorize_file, create_backup, is_safe_to_move, move_file, organize_files

    def get_directory_stats(self):
        """Get stats for organized directories"""
        stats = {}
        for category in settings.FILE_CATEGORIES.values():
            dir_path = settings.ORGANIZED_FILES_DIR / category
            if dir_path.exists():
                files = list(dir_path.glob('*'))
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                stats[category] = {
                    'file_count': len([f for f in files if f.is_file()]),
                    'total_size_mb': round(total_size / (1024 * 1024), 2),
                    'last_modified': max((f.stat().st_mtime for f in files if f.is_file()), default=0)
                }
        return stats

    def clean_empty_directories(self):
        """Remove empty directories"""
        removed_count = 0
        for d in settings.ORGANIZED_FILES_DIR.iterdir():
            if d.is_dir():
                try:
                    d.rmdir()
                    removed_count += 1
                    print(f"Removed empty directory: {d.name}")
                except OSError:
                    pass  # not empty, ignore
        return removed_count

# Convenience functions
def organize_downloads():
    fo = FileOrganizer()
    downloads = Path.home() / "Downloads"
    files = [f for f in downloads.iterdir() if f.is_file()] if downloads.exists() else []
    return fo.organize_files(files)

def organize_desktop():
    fo = FileOrganizer()
    desktop = Path.home() / "Desktop"
    files = [f for f in desktop.iterdir() if f.is_file()] if desktop.exists() else []
    return fo.organize_files(files)

def get_organizer_instance():
    """Return singleton FileOrganizer instance"""
    if not hasattr(get_organizer_instance, "_instance"):
        get_organizer_instance._instance = FileOrganizer()
    return get_organizer_instance._instance

# test
if __name__ == "__main__":
    stats = organize_downloads()
    print(stats)
    desktop_stats = organize_desktop()
    print(desktop_stats)
