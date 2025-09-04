# 📊 Desktop Smart Organizer

> Automate your file organization with a simple Python tool. This mini version focuses on automatic sorting of files in watched directories with optional backups and logging. Users can now choose directories at runtime or use default ones (Downloads, Desktop).

## ✨ Key Features

### Automatic File Organization
- Sort files by type (images, documents, videos, code, etc.)
- Optional backups before moving files

### Simple Configuration
- Easily set directories, backup preferences, and log levels via .env
- Choose custom watch directories at runtime

### Centralized Logging
- Logs to console and rotating file (data/logs/app.log)

## 📁 Project Structure

```
desktop-smart-organizer/
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 main.py                  # Entry point
├── 📂 config/
│   └── 📄 settings.py          # Configuration management
├── 📂 core/
│   └── 📄 file_organizer.py    # File scanning, categorization, and moving
└── 📂 utils/
    └── 📄 logger.py            # Centralized logging

```

## 🚀 Setup and Usage

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone git clone https://github.com/furoche04/Desktop-Smart-Organizer.git
   cd Desktop-Smart-Organizer
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
    # Edit .env as needed (custom watch directories, backup settings, log level)
   ```

5. **Run the organizer**
   ```bash
    python main.py
   ```

## 🔄 Next Steps & Enhancements

- **Screenshots & OCR**: integrate pyautogui and pytesseract,
- **System Monitoring**: track CPU, memory, disk usage with psutil,
- **GUI**: add a Tkinter interface to start/stop automation and display stats.
