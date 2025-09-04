import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Configuration settings for Desktop Smart Organizer"""
    
    def __init__(self):
        # Base paths
        self.PROJECT_ROOT = Path(__file__).parent.parent
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.SCREENSHOTS_DIR = self.DATA_DIR / "screenshots"
        self.ORGANIZED_FILES_DIR = self.DATA_DIR / "organized_files"
        self.LOGS_DIR = self.DATA_DIR / "logs"
        
        # Create directories if they don't exist
        self._create_directories()
        
        # File organization settings
        self.WATCH_DIRECTORIES = [
            Path.home() / "Downloads",
            Path.home() / "Desktop",
            # Add custom directories from env
            *self._get_custom_watch_dirs()
        ]
        
        self.FILE_CATEGORIES = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
            'presentations': ['.ppt', '.pptx', '.odp'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.c']
        }
        
        # Screenshot settings
        self.SCREENSHOT_FORMAT = os.getenv('SCREENSHOT_FORMAT', 'PNG')
        self.SCREENSHOT_QUALITY = int(os.getenv('SCREENSHOT_QUALITY', '85'))
        self.AUTO_SCREENSHOT_INTERVAL = int(os.getenv('AUTO_SCREENSHOT_INTERVAL', '300'))  # seconds
        
        # OCR settings
        self.OCR_LANGUAGE = os.getenv('OCR_LANGUAGE', 'eng')
        self.OCR_MIN_CONFIDENCE = int(os.getenv('OCR_MIN_CONFIDENCE', '50'))
        self.OCR_ENABLED = os.getenv('OCR_ENABLED', 'true').lower() == 'true'
        
        # System monitoring settings
        self.MONITOR_INTERVAL = int(os.getenv('MONITOR_INTERVAL', '60'))  # seconds
        self.CPU_THRESHOLD = int(os.getenv('CPU_THRESHOLD', '80'))  # percent
        self.MEMORY_THRESHOLD = int(os.getenv('MEMORY_THRESHOLD', '85'))  # percent
        self.DISK_THRESHOLD = int(os.getenv('DISK_THRESHOLD', '90'))  # percent
        
        # Automation settings
        self.AUTO_ORGANIZE_ENABLED = os.getenv('AUTO_ORGANIZE_ENABLED', 'true').lower() == 'true'
        self.AUTO_ORGANIZE_INTERVAL = int(os.getenv('AUTO_ORGANIZE_INTERVAL', '1800'))  # seconds
        self.BACKUP_BEFORE_ORGANIZE = os.getenv('BACKUP_BEFORE_ORGANIZE', 'true').lower() == 'true'
        
        # GUI settings
        self.WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '800'))
        self.WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
        self.THEME = os.getenv('THEME', 'light')  # light or dark
        
        # Logging settings
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', '10485760'))  # 10MB
        self.LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
        
        # Security settings (for keyring integration)
        self.USE_KEYRING = os.getenv('USE_KEYRING', 'false').lower() == 'true'
        self.APP_NAME = "DesktopSmartOrganizer"
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.DATA_DIR,
            self.SCREENSHOTS_DIR,
            self.ORGANIZED_FILES_DIR,
            self.LOGS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
        # Create subdirectories for organized files
        for category in self.FILE_CATEGORIES.keys():
            (self.ORGANIZED_FILES_DIR / category).mkdir(exist_ok=True)
    
    def _get_custom_watch_dirs(self):
        """Get custom watch directories from environment"""
        custom_dirs = os.getenv('CUSTOM_WATCH_DIRS', '')
        if custom_dirs:
            return [Path(dir_path.strip()) for dir_path in custom_dirs.split(',')]
        return []

    def get_category_for_extension(self, extension):
        """Get file category for a given extension"""
        extension = extension.lower()
        for category, extensions in self.FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        return 'others'
    
    def get_organized_path(self, category, filename):
        """Get the organized file path for a given category and filename"""
        return self.ORGANIZED_FILES_DIR / category / filename
    
    def update_setting(self, key, value):
        """Update a setting value dynamically"""
        if hasattr(self, key):
            setattr(self, key, value)
            return True
        return False
    
    def to_dict(self):
        """Convert settings to dictionary for easy serialization"""
        return {
            key: str(value) if isinstance(value, Path) else value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

# Global settings instance
settings = Settings()
