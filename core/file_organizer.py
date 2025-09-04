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

    def scan_directories(self):
        files = []
        watch_dirs = [Path.home() / "Downloads"]
        for d in watch_dirs:
            if d.exists():
                for f in d.iterdir():
                    if f.is_file():
                        files.append(f)
            else:
                logger.warning(f"Directory not found: {d}")
        return files

    def categorize_file(self, file_path: Path):
        ext = file_path.suffix.lower()
        category = settings.FILE_CATEGORIES.get(ext, 'Other')
        print(f"{file_path.name} categorized as {category}")
        return category

    def create_backup(self, file_path: Path):
        if not settings.BACKUP_BEFORE_MOVE:
            return None
        backup_dir = settings.ORGANIZED_FILES_DIR / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / file_path.name
        shutil.copy2(file_path, backup_path)  # might overwrite duplicates
        return backup_path

    def is_safe_to_move(self, file_path: Path) -> bool:
        """Check if file is safe to move"""
        try:
            # Check if file is being written (size check)
            initial_size = file_path.stat().st_size
            time.sleep(0.1)  # short wait
            current_size = file_path.stat().st_size
            if initial_size != current_size:
                print(f"{file_path.name} is being written to, skipping")
                return False

            # Check if file is too new
            age = time.time() - file_path.stat().st_mtime
            if age < 10:  # 10 seconds, might still be downloading
                print(f"{file_path.name} is very recent ({age:.1f}s), skipping")
                return False

            # Try opening file
            try:
                with open(file_path, 'rb') as f:
                    pass
            except PermissionError:
                print(f"{file_path.name} appears locked, skipping")
                return False

            return True
        except Exception as e:
            logger.error(f"Error checking {file_path}: {e}")
            return False

    def move_file(self, file_path: Path):
        if not self.is_safe_to_move(file_path):
            print(f"Skipping {file_path.name} - not safe")
            return
        category = self.categorize_file(file_path)
        dest_dir = settings.ORGANIZED_FILES_DIR / category
        dest_dir.mkdir(parents=True, exist_ok=True)
        self.create_backup(file_path)
        dest_path = dest_dir / file_path.name
        try:
            shutil.move(str(file_path), str(dest_path))
            self.organized_count += 1
            print(f"Moved {file_path.name} to {dest_dir}")
        except Exception as e:
            self.error_count += 1
            logger.error(f"Error moving {file_path}: {e}")

# test
if __name__ == "__main__":
    fo = FileOrganizer()
    files = fo.scan_directories()
    for f in files:
        fo.move_file(f)
