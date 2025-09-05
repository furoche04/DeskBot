import pyautogui
import pytesseract
from datetime import datetime
from pathlib import Path
from PIL import Image
from config.settings import settings, get_screenshots_dir

class OCRProcessor:
    def __init__(self):
        # Configure Tesseract executable path if provided
        if settings.TESSERACT_PATH:
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH

        # Create OCR results directory
        self.ocr_dir = get_screenshots_dir() / "ocr_results"
        self.ocr_dir.mkdir(parents=True, exist_ok=True)

    def take_screenshot(self) -> Path:
        """Take a screenshot and return its path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.{settings.SCREENSHOT_FORMAT.lower()}"
        filepath = get_screenshots_dir() / filename

        screenshot = pyautogui.screenshot()

        # Save screenshot with quality only for JPEG
        if settings.SCREENSHOT_FORMAT.lower() in ["jpg", "jpeg"]:
            screenshot.save(filepath, quality=settings.SCREENSHOT_QUALITY)
        else:
            screenshot.save(filepath)

        return filepath

    def run_ocr(self, image_path: Path) -> tuple[Path, str]:
        """Run OCR on a given image and save the text result"""
        try:
            img = Image.open(image_path)
            custom_config = f'--oem 3 --psm 6 -l {settings.OCR_LANGUAGE}'
            text = pytesseract.image_to_string(img, config=custom_config)
        except Exception as e:
            text = ""
            print(f"OCR failed for {image_path}: {e}")

        # Save text result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_file = self.ocr_dir / f"ocr_{timestamp}.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text.strip())

        return text_file, text.strip()

    def screenshot_and_ocr(self) -> tuple[Path, str]:
        """Take a screenshot and immediately process OCR"""
        screenshot_path = self.take_screenshot()
        return self.run_ocr(screenshot_path)

ocr_processor = OCRProcessor()