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
    window = MainWindow('0.4.3', 'test')
    window.show()
    app.processEvents()
    for i in range(window.stack.count()):
        window.nav.setCurrentRow(i)
        app.processEvents()
    assert '0.4.3' in window.windowTitle() and 'test' in window.windowTitle()
    assert LeadDialog(window).title is not None
    assert window.discover_button.text()
    assert len(window.source_rows) >= 140
    assert sum(1 for row in window.source_rows if row['name'].startswith('Belge #')) == 104
    assert all(not row['scan'] for row in window.source_rows if row['name'].startswith('Belge #'))
    assert sum(1 for row in window.source_rows if row['scan']) >= 5
    window.scan_result({'source': 'Kontrol', 'count': 1, 'candidates': [], 'examined': [{'title':'Deneme', 'url':'https://example.com', 'decision':'Elenmiş', 'reason':'Eşleşme yok'}]})
    assert window.scan_examined[0]['reason'] == 'Eşleşme yok'
    window.db.add_lead('Bilgisayar montaj hizmeti verilir', 'Test', 'https://example.com/offer', 'Ankara', 'Montaj yapıyorum')
    window.refresh(); window.nav.setCurrentRow(1); window.table.selectRow(0); app.processEvents()
    assert 'Hizmet sunma ilanı' in window.classification.text()
    window.note.setPlainText('Görüşme notu test'); window.save_lead(); app.processEvents()
    assert window.selected() is not None and window.note.toPlainText() == 'Görüşme notu test'
    assert 'kaydedildi' in window.save_status.text()
    window.refresh(); assert window.note.toPlainText() == 'Görüşme notu test'
    window.close()
print('SQLite and UI smoke checks passed')
