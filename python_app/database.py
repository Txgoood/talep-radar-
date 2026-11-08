import sqlite3
from PySide6.QtCore import QThread, Signal

# Arayüzü kilitlememek için veritabanı işlemleri QThread içinde yürütülür.
class DatabaseWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, query, params=()):
        super().__init__()
        self.query = query
        self.params = params

    def run(self):
        try:
            conn = sqlite3.connect("radardb.sqlite")
            cursor = conn.cursor()
            cursor.execute(self.query, self.params)
            conn.commit()
            result = cursor.fetchall()
            conn.close()
            self.finished.emit({"data": result})
        except Exception as e:
            self.error.emit(str(e))
