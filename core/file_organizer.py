import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import logging

from config.settings import settings

logger = logging.getLogger(__name__)

class FileOrganizer:
    """Handles automatic file organization and sorting"""
    
    def __init__(self):
        self.organized_count = 0
        self.error_count = 0
        self.last_run = None
        self.backup_enabled = settings.BACKUP_BEFORE_ORGANIZE
        
    def scan_directories(self) -> List[Path]:
        """Scan watch directories for files to organize"""
        files_to_organize = []
        for watch_dir in settings.WATCH_DIRECTORIES:
            if not watch_dir.exists():
                logger.warning(f"Watch directory does not exist: {watch_dir}")
                continue
            try:
                for file_path in watch_dir.iterdir():
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        files_to_organize.append(file_path)
            except PermissionError:
                logger.error(f"Permission denied accessing: {watch_dir}")
            except Exception as e:
                logger.error(f"Error scanning {watch_dir}: {str(e)}")
        logger.info(f"Found {len(files_to_organize)} files to potentially organize")
        return files_to_organize
    
    def categorize_file(self, file_path: Path) -> str:
        """Determine the category for a file based on its extension"""
        return settings.get_category_for_extension(file_path.suffix)
    
    def is_safe_to_move(self, file_path: Path) -> bool:
        """Check if file is safe to move (not in use, not system file, etc.)"""
        try:
            initial_size = file_path.stat().st_size
            time.sleep(0.1)
            current_size = file_path.stat().st_size
            if initial_size != current_size:
                logger.debug(f"File {file_path.name} appears to be actively written to")
                return False
            file_age = time.time() - file_path.stat().st_mtime
            if file_age < 30:
                logger.debug(f"File {file_path.name} is too recent (age: {file_age}s)")
                return False
            try:
                with open(file_path, 'rb'):
                    pass
            except PermissionError:
                logger.debug(f"File {file_path.name} appears to be locked")
                return False
            return True
        except Exception as e:
            logger.error(f"Error checking if file is safe to move: {str(e)}")
            return False
    
    def create_backup(self, file_path: Path) -> Optional[Path]:
        """Create a backup of the file before moving"""
        if not self.backup_enabled:
            return None
        try:
            backup_dir = settings.DATA_DIR / "backups" / datetime.now().strftime("%Y%m%d")
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / file_path.name
            counter = 1
            while backup_path.exists():
                stem, suffix = file_path.stem, file_path.suffix
                backup_path = backup_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            shutil.copy2(file_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup for {file_path.name}: {str(e)}")
            return None
    
    def move_file(self, file_path: Path, category: str) -> bool:
        """Move file to organized directory"""
        try:
            dest_dir = settings.ORGANIZED_FILES_DIR / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / file_path.name
            counter = 1
            while dest_path.exists():
                stem, suffix = file_path.stem, file_path.suffix
                dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            self.create_backup(file_path)
            shutil.move(str(file_path), str(dest_path))
            logger.info(f"Moved {file_path.name} to {category}/{dest_path.name}")
            self.organized_count += 1
            return True
        except Exception as e:
            logger.error(f"Failed to move {file_path.name}: {str(e)}")
            self.error_count += 1
            return False
    
    def organize_files(self, file_list: Optional[List[Path]] = None) -> Dict[str, int]:
        """Organize files from watch directories or provided list"""
        start_time = datetime.now()
        self.organized_count = 0
        self.error_count = 0
        files_to_process = file_list if file_list else self.scan_directories()
        if not files_to_process:
            logger.info("No files to organize")
            return self.get_organization_stats()
        logger.info(f"Starting organization of {len(files_to_process)} files")
        category_counts = {}
        for file_path in files_to_process:
            try:
                if not file_path.exists():
                    continue
                if not self.is_safe_to_move(file_path):
                    logger.debug(f"Skipping {file_path.name} - not safe to move")
                    continue
                category = self.categorize_file(file_path)
                if self.move_file(file_path, category):
                    category_counts[category] = category_counts.get(category, 0) + 1
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                self.error_count += 1
        self.last_run = start_time
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Organization complete. Organized: {self.organized_count}, "
                    f"Errors: {self.error_count}, Duration: {duration:.2f}s")
        return self.get_organization_stats(category_counts)
    
    def organize_single_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
        if not self.is_safe_to_move(file_path):
            logger.warning(f"File not safe to move: {file_path}")
            return False
        category = self.categorize_file(file_path)
        return self.move_file(file_path, category)
    
    def get_organization_stats(self, category_counts: Optional[Dict[str, int]] = None) -> Dict[str, int]:
        stats = {
            'total_organized': self.organized_count,
            'total_errors': self.error_count,
            'last_run': self.last_run.isoformat() if self.last_run else None
        }
        if category_counts:
            stats['categories'] = category_counts
        return stats
    
    def get_directory_stats(self) -> Dict[str, Dict]:
        stats = {}
        for category in settings.FILE_CATEGORIES.keys():
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
    
    def clean_empty_directories(self) -> int:
        removed_count = 0
        for category_dir in settings.ORGANIZED_FILES_DIR.iterdir():
            if category_dir.is_dir():
                try:
                    category_dir.rmdir()
                    removed_count += 1
                    logger.info(f"Removed empty directory: {category_dir.name}")
                except OSError:
                    pass  # not empty
        return removed_count

# Convenience functions
def organize_downloads():
    fo = FileOrganizer()
    downloads_path = Path.home() / "Downloads"
    files = [f for f in downloads_path.iterdir() if f.is_file()] if downloads_path.exists() else []
    return fo.organize_files(files)

def organize_desktop():
    fo = FileOrganizer()
    desktop_path = Path.home() / "Desktop"
    files = [f for f in desktop_path.iterdir() if f.is_file()] if desktop_path.exists() else []
    return fo.organize_files(files)

def get_organizer_instance():
    if not hasattr(get_organizer_instance, '_instance'):
        get_organizer_instance._instance = FileOrganizer()
    return get_organizer_instance._instance
