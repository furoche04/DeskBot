import os
from pathlib import Path
import logging

class Settings:
    FILE_CATEGORIES = {
        '.txt': 'Text',
        '.jpg': 'Images',
        '.png': 'Images',
        '.pdf': 'Documents',
    }

settings = Settings()

logger = logging.getLogger(__name__)

class FileOrganizer:
    """Basic skeleton for file organizer"""

    def __init__(self):
        self.organized_count = 0
        self.error_count = 0

    def scan_directories(self):
        """Scan directories for files (placeholder)"""
        files = []
        watch_dirs = [Path.home() / "Downloads"]  #hc
        
        for d in watch_dirs:
            if d.exists():
                for f in d.iterdir():
                    if f.is_file():
                        files.append(f)
            else:
                logger.warning(f"Directory not found: {d}")
        
        return files

    def categorize_file(self, file_path: Path):
        """Categorize file based on extension (simple version)"""
        ext = file_path.suffix.lower()
        category = settings.FILE_CATEGORIES.get(ext, 'Other')

        print(f"{file_path.name} categorized as {category}")
        return category

# test
if __name__ == "__main__":
    fo = FileOrganizer()
    files = fo.scan_directories()
    for f in files:
        fo.categorize_file(f)
