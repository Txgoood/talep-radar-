import os
import tempfile
from pathlib import Path

# Test verileri gerçek kullanıcı kayıtlarından ayrı tutulur.
with tempfile.TemporaryDirectory() as directory:
    os.environ['LOCALAPPDATA'] = directory
    from PySide6.QtWidgets import QApplication
    from database import Database
    from ui.main_window import MainWindow, LeadDialog
    app = QApplication([])
    db = Database(Path(directory) / 'test.sqlite')
    db.add_lead('SSD montaj', 'Test', 'https://example.com', 'Kartal', 'Talep')
    row = db.leads()[0]
    db.update_lead(row['id'], 'Randevu', 'Akşam')
    assert db.leads()[0]['note'] == 'Akşam'
    db.set_setting('stop_sending', '1')
    assert Database(Path(directory) / 'test.sqlite').get_setting('stop_sending') == '1'
    window = MainWindow('0.3.0', 'test')
    window.show()
    app.processEvents()
    for i in range(window.stack.count()):
        window.nav.setCurrentRow(i)
        app.processEvents()
    assert '0.3.0' in window.windowTitle() and 'test' in window.windowTitle()
    assert LeadDialog(window).title is not None
    window.close()
print('SQLite and UI smoke checks passed')
