from gui.interface import run_gui
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting DeskBot...")
    run_gui()
