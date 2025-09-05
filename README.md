# 🗂️ DeskBot

> Automate your file organization with a simple Python tool. This mini version focuses on automatic sorting of files in watched directories with optional backups and logging. Users can now choose directories at runtime or use default ones (Downloads, Desktop).

## ✨ Key Features

### Automatic File Organization
- Sort files by type (images, documents, videos, code, etc.)
- Optional backups before moving files

### Custom Directory Selection
- Choose directories to organize at runtime via GUI
- Supports default directories (Downloads, Desktop) as well as any folder

### OCR & Screenshot
- Take screenshots and extract text via OCR
- Choose OCR language for multi-language support
- OCR results are saved to the project data folder and displayed in the GUI

### Simple Configuration
- Easily set directories, backup preferences, log levels, screenshot and OCR settings via .env

### Centralized Logging
- Logs to console and rotating file (data/logs/app.log)
- GUI displays logs in real-time for user feedback

## 📁 Project Structure

```
DeskBot/
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .env.example           # Example .env file
├── 📄 main.py                # Entry point
├── 📂 config/
│ └── 📄 settings.py          # Centralized settings
├── 📂 core/
│ ├── 📄 file_organizer.py    # File scanning, categorization, and moving
│ ├── 📄 system_monitor.py    # System resource monitoring
│ └── 📄 ocr_processor.py     # Screenshot capture and OCR processing
├── 📂 data/
│ ├── 📂 backups/             # Backups
│ ├── 📂 logs/                # Logs
│ ├── 📂 organized_files/     # Organized files
│ └── 📂 screenshots/         # Screenshots
├── 📂 demo_files/            # Dummy files for testing purposes
├── 📂 gui/
│ └── 📄 interface.py         # GUI interface
└── 📂 utils/
  └── 📄 logger.py            # Centralized logging

```

## 🗂️ Demo Files for Testing

A demo_files folder is included in this repository for easy testing of the Desktop Smart Organizer.
- Contains a mix of documents, images, spreadsheets, code files, videos, and archives
- Includes some unrecognized or unusual file extensions to test the "others" category

## 🚀 Setup and Usage

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning)
- Tesseract OCR installed for OCR functionality (optional, see .env for TESSERACT_PATH)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/furoche04/DeskBot.git
   cd DeskBot
   ```

2. **Create virtual environment** (recommended)
   ```bash
    python -m venv venv
    source venv/bin/activate    # Linux/macOS
    venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy and edit configuration**
   ```bash
    cp .env.example .env
    # Edit .env as needed (backup settings, log level, OCR language, screenshot format, etc.)
   ```

5. **Run the organizer**
   ```bash
    python main.py
   ```

## 🔄 Next Steps & Enhancements

- **TBA**