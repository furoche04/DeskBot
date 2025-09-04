import os
from pathlib import Path
import logging

# TODO: add settings import later
# from config.settings import settings

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

# test
if __name__ == "__main__":
    fo = FileOrganizer()
    print(fo.scan_directories()) 

