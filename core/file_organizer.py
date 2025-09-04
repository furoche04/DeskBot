import os
from pathlib import Path
import shutil
import logging
from datetime import datetime

# Temporary settings
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
    """Basic skeleton for file organizer"""

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
        """Create backup (basic)"""
        if not settings.BACKUP_BEFORE_MOVE:
            return None
        backup_dir = settings.ORGANIZED_FILES_DIR / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / file_path.name
        # overwrite if duplicate names
        shutil.copy2(file_path, backup_path)
        return backup_path

    def move_file(self, file_path: Path):
        """Move file to categorized folder"""
        category = self.categorize_file(file_path)
        dest_dir = settings.ORGANIZED_FILES_DIR / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        # create backup first
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
