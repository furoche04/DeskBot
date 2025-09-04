import psutil
from datetime import datetime

class SystemMonitor:
    """Simple system resource monitoring"""

    def __init__(self):
        self.last_check = None
        self.cpu_percent = 0
        self.memory_percent = 0
        self.disk_percent = 0

    def update_stats(self):
        """Update system stats"""
        self.last_check = datetime.now()
        self.cpu_percent = psutil.cpu_percent(interval=1)
        self.memory_percent = psutil.virtual_memory().percent
        self.disk_percent = psutil.disk_usage('/').percent

    def get_stats(self):
        """Return current system stats as a dictionary"""
        self.update_stats()
        return {
            'timestamp': self.last_check.isoformat(),
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'disk_percent': self.disk_percent
        }


if __name__ == "__main__":
    monitor = SystemMonitor()
    stats = monitor.get_stats()
    print("System stats:")
    for key, value in stats.items():
        print(f"{key}: {value}")