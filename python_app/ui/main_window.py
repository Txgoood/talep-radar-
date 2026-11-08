from PySide6.QtCore import Qt, QUrl, QThread, Signal, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QListWidget, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QFormLayout, QLineEdit, QTextEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox, QSplitter)
from database import Database
from scanner import SOURCES, ScanError, fetch_feed

STYLE = '''
QWidget { background:#0B1220; color:#E8EEF7; font-family:Segoe UI; font-size:13px; }
QFrame#side, QListWidget {background:#142033; border:0;}
QLabel#heading {font-size:20px; font-weight:700; color:#A5C9FF;}
QLabel#muted {color:#A6B4C8;}
QPushButton {background:#25354B; color:#E8EEF7; padding:9px; border:1px solid #344761; border-radius:4px;}
QPushButton:hover {background:#344C6B;} QPushButton#primary {background:#22C55E;color:#071510;font-weight:bold;}
QPushButton#danger {color:#FBA8A1; border:1px solid #F87171;background:#33202A;}
QLineEdit,QTextEdit,QComboBox,QTableWidget {background:#080F1D; border:1px solid #24354D; padding:7px; selection-background-color:#315883;}
QHeaderView::section {background:#1C2B41; color:#C7D4E8; padding:8px; border:0;}
QListWidget::item {padding:11px;} QListWidget::item:selected {background:#60A5FA;color:#07111F;}
'''

class ScanWorker(QThread):
    result = Signal(dict)
    source_error = Signal(str, str)
    def run(self):
        for source in SOURCES:
            try:
                self.result.emit(fetch_feed(source))
            except Exception as exc:
                self.source_error.emit(source, str(exc))

class LeadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle('Manuel talep ekle'); self.resize(520, 400)
        form = QFormLayout(self)
        self.title = QLineEdit(); self.source = QLineEdit(); self.url = QLineEdit(); self.location = QLineEdit(); self.description = QTextEdit()
        for name, field in [('Başlık *',self.title),('Kaynak',self.source),('Kaynak bağlantısı',self.url),('Konum',self.location),('Talep metni',self.description)]: form.addRow(name,field)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); form.addRow(buttons)
    def accept(self):
        if not self.title.text().strip(): QMessageBox.warning(self,'Eksik bilgi','Talep başlığını girin.'); return
        super().accept()

class MainWindow(QMainWindow):
    def __init__(self, version, build):
        super().__init__(); self.version=version; self.build=build; self.db=Database(); self.rows=[]; self.scan_worker=None; self.scan_messages=[]
        self.setWindowTitle(f'Talep Radarı · v{version} · Build {build}'); self.resize(1440,900); self.setMinimumSize(900,600); self.setStyleSheet(STYLE)
        root=QWidget(); self.setCentralWidget(root); layout=QHBoxLayout(root); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)
        side=QWidget(); side.setFixedWidth(225); side.setStyleSheet('background:#142033'); sl=QVBoxLayout(side)
        logo=QLabel('● TALEP RADARI'); logo.setObjectName('heading'); sl.addWidget(logo)
        subtitle=QLabel('Masaüstü · Yerel SQLite'); subtitle.setObjectName('muted'); sl.addWidget(subtitle)
        self.stop=QPushButton(); self.stop.setObjectName('danger'); self.stop.clicked.connect(self.toggle_stop); sl.addWidget(self.stop)
        self.nav=QListWidget(); self.nav.addItems(['Özet','Talepler','Görüşmeler','Onay Bekleyenler','Kaynaklar','Raporlar','Ayarlar','Telegram Tanı']); sl.addWidget(self.nav)
        sl.addWidget(QLabel('Operatör · Yerel kullanım')); layout.addWidget(side)
        self.stack=QStackedWidget(); layout.addWidget(self.stack,1)
        self.dashboard=self.make_dashboard(); self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.make_leads())
        self.stack.addWidget(self.placeholder('Görüşmeler','Telegram ve kaynak entegrasyonu henüz kurulmadı.'))
        self.stack.addWidget(self.placeholder('Onay Bekleyenler','Otomatik gönderim henüz desteklenmiyor.'))
        self.stack.addWidget(self.make_sources())
        self.stack.addWidget(self.placeholder('Raporlar','Gerçek kayıtlar oluştukça raporlar geliştirilecektir.'))
        self.stack.addWidget(self.make_settings())
        self.stack.addWidget(self.placeholder('Telegram Tanı','Telegram bağlantısı henüz uygulanmadı.'))
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex); self.nav.setCurrentRow(0)
        from PySide6.QtGui import QShortcut, QKeySequence
        self.scan_shortcut=QShortcut(QKeySequence('F5'), self); self.scan_shortcut.activated.connect(self.start_scan)
        self.update_stop(); self.refresh()
        self.timer=QTimer(self); self.timer.setInterval(30*60*1000); self.timer.timeout.connect(self.start_scan)
        self.auto_scan.setChecked(self.db.get_setting('auto_scan','0') == '1')
        if self.auto_scan.isChecked(): self.timer.start()
    def page(self, title, subtitle=''):
        w=QWidget(); v=QVBoxLayout(w); v.setContentsMargins(22,18,22,18)
        h=QLabel(title); h.setObjectName('heading'); v.addWidget(h)
        if subtitle:
            label=QLabel(subtitle); label.setObjectName('muted'); label.setWordWrap(True); v.addWidget(label)
        return w,v
    def placeholder(self,title,subtitle):
        w,v=self.page(title,subtitle); v.addStretch(); return w
    def make_dashboard(self):
        w,v=self.page('Genel Özet ve Durum Radarı','Gerçek kayıtlar · Kaynak erişim durumu tarama sonucuna göre gösterilir')
        top=QHBoxLayout(); self.summary=QLabel(); self.summary.setStyleSheet('background:#142033;padding:20px;font-size:16px;'); top.addWidget(self.summary,1)
        self.scan_button=QPushButton('⟳  Manuel Tara (F5)'); self.scan_button.setObjectName('primary'); self.scan_button.clicked.connect(self.start_scan); top.addWidget(self.scan_button); v.addLayout(top)
        self.scan_status=QLabel('Tarama henüz yapılmadı. Akışın sunduğu son kayıtlar incelenir.'); self.scan_status.setWordWrap(True); self.scan_status.setStyleSheet('background:#142033;padding:15px;'); v.addWidget(self.scan_status)
        button=QPushButton('Talepleri İncele'); button.clicked.connect(lambda:self.nav.setCurrentRow(1)); v.addWidget(button)
        v.addWidget(QLabel('Telegram: Bağlı değil   |   Yerel model: Kullanılmıyor   |   Gönderim: Desteklenmiyor'))
        v.addStretch(); return w
    def make_sources(self):
        w,v=self.page('Kaynaklar ve Adaptör Yetenek Matrisi','RSS keşfi · Salt okunur · Kaynakların erişimi her taramada doğrulanır')
        for name,url in SOURCES.items():
            label=QLabel(f'{name}    •    RSS okuma denemesi    •    Yanıt gönderme: Desteklenmiyor\n{url}')
            label.setWordWrap(True); label.setStyleSheet('background:#142033;padding:15px;'); v.addWidget(label)
        from PySide6.QtWidgets import QCheckBox
        self.auto_scan=QCheckBox('30 dakikada bir tara (uygulama açıkken)'); self.auto_scan.toggled.connect(self.set_auto_scan); v.addWidget(self.auto_scan)
        hint=QLabel('Her kaynak yalnızca akışında verdiği son kayıtları sunar (çoğunlukla 20). Olası talepler ve daha geniş inceleme adayları listelenir; gerçek ihtiyaç ve konumu kontrol edin. Erişim hatası, talep yok demek değildir.')
        hint.setWordWrap(True); v.addWidget(hint); v.addStretch(); return w
    def set_auto_scan(self, checked):
        self.db.set_setting('auto_scan','1' if checked else '0')
        if hasattr(self,'timer'):
            self.timer.start() if checked else self.timer.stop()
    def start_scan(self):
        if self.scan_worker and self.scan_worker.isRunning(): return
        self.scan_messages=[]; self.scan_status.setText('Kaynaklar taranıyor…'); self.scan_button.setEnabled(False)
        self.scan_worker=ScanWorker(self); self.scan_worker.result.connect(self.scan_result); self.scan_worker.source_error.connect(self.scan_error); self.scan_worker.finished.connect(self.scan_finished); self.scan_worker.start()
    def scan_result(self, result):
        try:
            added=self.db.save_scan(result['source'],result['candidates'])
            self.scan_messages.append(f"{result['source']}: {result['count']} kayıt incelendi, {len(result['candidates'])} olası/inceleme adayı, {added} yeni kayıt. Yalnızca RSS akışının sunduğu kayıtlar incelendi.")
        except Exception:
            self.scan_messages.append(f"{result['source']}: sonuçlar kaydedilemedi; tekrar deneyin.")
    def scan_error(self, source, message):
        self.scan_messages.append(f'{source}: {message}')
    def scan_finished(self):
        self.scan_status.setText('\n'.join(self.scan_messages)); self.scan_button.setEnabled(True); self.refresh()
    def closeEvent(self, event):
        if self.scan_worker and self.scan_worker.isRunning():
            QMessageBox.information(self, 'Tarama devam ediyor', 'Tarama tamamlandığında pencereyi kapatabilirsiniz.'); event.ignore(); return
        event.accept()
    def make_leads(self):
        w,v=self.page('Talepler','Taranan adayları ve manuel eklediğiniz talepleri inceleyin. Konum ve hizmet ihtiyacı doğrulanmalıdır.')
        actions=QHBoxLayout(); add=QPushButton('+ Manuel talep ekle'); add.setObjectName('primary'); add.clicked.connect(self.add_lead); actions.addWidget(add)
        self.search=QLineEdit(); self.search.setPlaceholderText('Talep, kaynak veya konum ara'); self.search.textChanged.connect(self.refresh); actions.addWidget(self.search); v.addLayout(actions)
        splitter=QSplitter(); self.table=QTableWidget(0,5); self.table.setHorizontalHeaderLabels(['ID','BAŞLIK','KAYNAK','KONUM','DURUM']); self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch); self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows); self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); self.table.itemSelectionChanged.connect(self.show_detail); splitter.addWidget(self.table)
        detail=QWidget(); d=QVBoxLayout(detail); self.detail_title=QLabel('Bir talep seçin'); self.detail_title.setWordWrap(True); d.addWidget(self.detail_title)
        self.desc=QLabel(''); self.desc.setWordWrap(True); d.addWidget(self.desc)
        self.status=QComboBox(); self.status.addItems(['Yeni','İncelenecek','Cevap bekleniyor','Kullanıcı devraldı','Randevu','İş alındı','Tamamlandı','Uygun değil','Kapandı']); d.addWidget(self.status)
        self.note=QTextEdit(); self.note.setPlaceholderText('Görüşme notları'); d.addWidget(self.note)
        save=QPushButton('Durumu ve notu kaydet'); save.setObjectName('primary'); save.clicked.connect(self.save_lead); d.addWidget(save)
        open_url=QPushButton('Kaynakta aç'); open_url.clicked.connect(self.open_source); d.addWidget(open_url); splitter.addWidget(detail); splitter.setSizes([800,400]); v.addWidget(splitter,1); return w
    def make_settings(self):
        w,v=self.page('Ayarlar','Uygulama bilgisi ve yerel veri')
        v.addWidget(QLabel(f'Talep Radarı  ·  Sürüm {self.version}  ·  Build {self.build}'))
        v.addWidget(QLabel(f'Veritabanı: {self.db.path}')); v.addWidget(QLabel('Telegram ve yerel model henüz uygulanmadı.')); v.addStretch(); return w
    def refresh(self):
        self.rows=self.db.leads(); self.summary.setText(f'Kayıtlı talepler  {len(self.rows)}     ·     Yeni  {sum(r["status"] == "Yeni" for r in self.rows)}')
        query=self.search.text().casefold() if hasattr(self,'search') else ''
        self.filtered=[r for r in self.rows if query in ' '.join(str(r[x]) for x in ('title','source','location','description')).casefold()]
        self.table.setRowCount(len(self.filtered))
        for i,r in enumerate(self.filtered):
            for j,key in enumerate(('id','title','source','location','status')): self.table.setItem(i,j,QTableWidgetItem(str(r[key])))
        self.detail_title.setText('Bir talep seçin'); self.desc.clear(); self.note.clear()
    def selected(self):
        i=self.table.currentRow(); return self.filtered[i] if 0 <= i < len(self.filtered) else None
    def show_detail(self):
        r=self.selected()
        if r:
            self.detail_title.setText(f'Talep #{r["id"]} · {r["title"]}'); self.desc.setText(r['description'] or 'Talep metni eklenmedi.'); self.status.setCurrentText(r['status']); self.note.setPlainText(r['note'])
    def add_lead(self):
        d=LeadDialog(self)
        if d.exec():
            self.db.add_lead(d.title.text(),d.source.text(),d.url.text(),d.location.text(),d.description.toPlainText()); self.refresh()
    def save_lead(self):
        r=self.selected()
        if r: self.db.update_lead(r['id'],self.status.currentText(),self.note.toPlainText()); self.refresh()
    def open_source(self):
        r=self.selected()
        if not r: return
        url=QUrl(r['url'])
        if url.scheme() not in ('http','https') or not url.host(): QMessageBox.warning(self,'Geçersiz bağlantı','http veya https ile başlayan bir kaynak bağlantısı gerekli.'); return
        QDesktopServices.openUrl(url)
    def toggle_stop(self):
        self.db.set_setting('stop_sending', '0' if self.db.get_setting('stop_sending','1') == '1' else '1'); self.update_stop()
    def update_stop(self):
        active=self.db.get_setting('stop_sending','1') == '1'
        self.stop.setText('⏻ GÖNDERİM KİLİDİ: ' + ('AKTİF' if active else 'KAPALI'))
        self.stop.setToolTip('Gönderim henüz uygulanmadı. Kilit tercihi yerel olarak saklanır.')
