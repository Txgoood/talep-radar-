import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

# Talep Radarı ana giriş noktası
# Uygulama PySide6 ile masaüstü ortamında çalışacak şekilde tasarlanmıştır.

def main():
    app = QApplication(sys.argv)
    
    # Stil tanımlamaları (Stitch Tasarım Dili için yer tutucu)
    # Tasarımlar sağlandığında burası güncellenecektir.
    app.setStyleSheet("""
        QMainWindow { background-color: #ffffff; }
        QPushButton { background-color: #000000; color: white; border-radius: 4px; padding: 5px; }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
