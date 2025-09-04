from core.file_organizer import FileOrganizer, organize_downloads, organize_desktop
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def main():
    fo = FileOrganizer()
    
    try:
        # Scan directories
        files = fo.scan_directories()
        logger.info(f"Found {len(files)} files to organize:")
        for f in files:
            logger.info(f"  - {f.name}")
        
        # Organize files
        stats = fo.organize_files(files)
        logger.info("Organization stats:")
        for key, value in stats.items():
            logger.info(f"{key}: {value}")
        
        # Optional: convenience functions
        # stats_downloads = organize_downloads()
        # stats_desktop = organize_desktop()
        
    except Exception as e:
        logger.error(f"Error running FileOrganizer: {e}")

if __name__ == "__main__":
    main()
