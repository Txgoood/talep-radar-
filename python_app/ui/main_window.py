from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Talep Radarı")
        self.resize(800, 600)

        # Ana içerik alanı
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Stitch tasarımı buraya eklenecektir
        self.label = QLabel("Talep Radarı Arayüzü (Stitch Tasarım Bekleniyor)")
        self.layout.addWidget(self.label)
