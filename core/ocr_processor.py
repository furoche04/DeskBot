import pyautogui
import pytesseract
from datetime import datetime
from pathlib import Path
from PIL import Image
from core.settings import settings, get_screenshots_dir, get_tesseract_path

class OCRProcessor:
    def __init__(self):
        # Configure tesseract path if provided
        if settings.TESSERACT_PATH:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH

        # Create OCR results directory
        self.ocr_dir = get_screenshots_dir() / "ocr_results"
        self.ocr_dir.mkdir(parents=True, exist_ok=True)

    def take_screenshot(self):
        """Take a screenshot and return its path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.{settings.SCREENSHOT_FORMAT.lower()}"
        filepath = get_screenshots_dir() / filename
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath, quality=settings.SCREENSHOT_QUALITY)
        return filepath

    def run_ocr(self, image_path: Path):
        """Run OCR on a given image and save results"""
        img = Image.open(image_path)
        custom_config = f'--oem 3 --psm 6 -l {settings.OCR_LANGUAGE}'
        text = pytesseract.image_to_string(img, config=custom_config)

        # Save text result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_file = self.ocr_dir / f"ocr_{timestamp}.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text.strip())

        return text_file, text.strip()

    def screenshot_and_ocr(self):
        """Take screenshot and immediately process OCR"""
        screenshot_path = self.take_screenshot()
        return self.run_ocr(screenshot_path)

# Singleton instance
ocr_processor = OCRProcessor()