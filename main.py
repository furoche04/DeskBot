from core.file_organizer import FileOrganizer
from utils.logger import setup_logger
from pathlib import Path

logger = setup_logger(__name__)

def get_user_directories():
    """Ask user for directories to watch or use defaults"""
    use_defaults = input("Use default directories (Downloads + Desktop)? [Y/n]: ").strip().lower()
    
    if use_defaults in ("", "y", "yes"):
        return None  # FileOrganizer will use WATCH_DIRECTORIES from settings
    
    dirs_input = input("Enter directories to watch (comma-separated): ").strip()
    dirs = [Path(d.strip()) for d in dirs_input.split(",") if d.strip()]
    
    if not dirs:
        logger.warning("No valid directories entered, falling back to defaults.")
        return None
    
    return dirs

def main():
    fo = FileOrganizer()
    
    # Ask user for directories
    custom_dirs = get_user_directories()
    
    try:
        # Scan directories
        files = fo.scan_directories() if not custom_dirs else fo.scan_directories_from_list(custom_dirs)
        logger.info(f"Found {len(files)} files to organize:")
        for f in files:
            logger.info(f"  - {f.name}")
        
        # Organize files
        stats = fo.organize_files(files)
        logger.info("Organization stats:")
        for key, value in stats.items():
            logger.info(f"{key}: {value}")
        
    except Exception as e:
        logger.error(f"Error running FileOrganizer: {e}")

if __name__ == "__main__":
    main()
