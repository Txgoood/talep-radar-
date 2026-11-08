import os
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

from version import VERSION, BUILD

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Talep Radarı')
    app.setStyle('Fusion')
    window = MainWindow(VERSION, BUILD)
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
