import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from pathlib import Path
from ui.main_window import MainWindow

from version import VERSION, BUILD

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Talep Radarı')
    icon_root = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    app.setWindowIcon(QIcon(str(icon_root / 'app.ico')))
    app.setStyle('Fusion')
    window = MainWindow(VERSION, BUILD)
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
