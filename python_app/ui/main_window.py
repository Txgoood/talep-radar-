from PySide6.QtCore import Qt, QUrl, QThread, Signal, QTimer
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QListWidget, QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QFormLayout, QLineEdit, QTextEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox, QSplitter)
from database import Database
from source_catalog import CATALOG
from imported_catalog import IMPORTED
from scanner import SOURCES, ScanError, fetch_feed, validate_feed_url, classify_detail

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
    def __init__(self, sources, parent=None):
        super().__init__(parent); self.sources = sources
    def run(self):
        for source, url in self.sources.items():
            try:
                self.result.emit(fetch_feed(source, url=url))
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
        super().__init__(); self.version=version; self.build=build; self.db=Database(); self.rows=[]; self.scan_worker=None; self.scan_messages=[]; self.scan_examined=[]
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
        audit=QPushButton('Son taramada incelenenleri göster'); audit.clicked.connect(self.show_scan_audit); v.addWidget(audit)
        button=QPushButton('Talepleri İncele'); button.clicked.connect(lambda:self.nav.setCurrentRow(1)); v.addWidget(button)
        v.addWidget(QLabel('Telegram: Bağlı değil   |   Yerel model: Kullanılmıyor   |   Gönderim: Desteklenmiyor'))
        v.addStretch(); return w
    def make_sources(self):
        w,v=self.page('Kaynaklar ve Adaptör Yetenek Matrisi','RSS/Atom keşfi · Salt okunur · Erişim tarama sırasında doğrulanır')
        self.source_table=QTableWidget(0,3); self.source_table.setHorizontalHeaderLabels(['KAYNAK','ADRES','ERİŞİM DURUMU'])
        self.source_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.source_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows); self.source_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        v.addWidget(self.source_table,1)
        actions=QHBoxLayout(); add=QPushButton('+ RSS Kaynağı Ekle'); add.setObjectName('primary'); add.clicked.connect(self.add_source); actions.addWidget(add)
        open_button=QPushButton('Seçilen kaynağı aç'); open_button.clicked.connect(self.open_catalog_source); actions.addWidget(open_button)
        remove=QPushButton('Seçilen özel kaynağı kaldır'); remove.clicked.connect(self.remove_source); actions.addWidget(remove); v.addLayout(actions)
        from PySide6.QtWidgets import QCheckBox
        self.auto_scan=QCheckBox('30 dakikada bir tara (uygulama açıkken)'); self.auto_scan.toggled.connect(self.set_auto_scan); v.addWidget(self.auto_scan)
        hint=QLabel('Yalnızca RSS olarak işaretli kaynaklar taranır. Belge adresleri araştırma listesidir; adres ve içerik doğrulanmamıştır. Hesapla giriş ve otomatik gönderim desteklenmiyor.')
        hint.setWordWrap(True); v.addWidget(hint); self.refresh_sources(); return w
    def refresh_sources(self):
        self.source_rows=[{'name':name,'url':url,'builtin':True,'scan':True,'state':'RSS · test edilmedi'} for name,url in SOURCES.items()]
        self.source_rows += [dict(row, builtin=False, scan=True, state='RSS · test edilmedi') for row in self.db.custom_sources()]
        self.source_rows += [{'name':name,'url':url,'builtin':True,'scan':False,'state':state} for name,url,state in CATALOG + IMPORTED]
        self.source_table.setRowCount(len(self.source_rows))
        for i,row in enumerate(self.source_rows):
            for j,value in enumerate((row['name'],row['url'],row['state'])):
                self.source_table.setItem(i,j,QTableWidgetItem(value))
    def open_catalog_source(self):
        i=self.source_table.currentRow()
        if not (0 <= i < len(self.source_rows)): return
        row=self.source_rows[i]
        if row['name'].startswith('Belge #'):
            choice=QMessageBox.question(self,'Doğrulanmamış bağlantı','Bu adres kullanıcı listesinden alındı, erişimi ve içeriği doğrulanmadı. Tarayıcıda açılsın mı?')
            if choice != QMessageBox.StandardButton.Yes: return
        QDesktopServices.openUrl(QUrl(row['url']))
    def add_source(self):
        dialog=QDialog(self); dialog.setWindowTitle('Özel RSS kaynağı ekle'); dialog.resize(580,200); form=QFormLayout(dialog)
        name=QLineEdit(); url=QLineEdit(); url.setPlaceholderText('https://site.example/rss')
        form.addRow('Kaynak adı',name); form.addRow('HTTPS RSS/Atom adresi',url)
        note=QLabel('Giriş bilgisi veya gizli anahtar içeren adresler eklenmez.'); note.setWordWrap(True); form.addRow(note)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept); buttons.rejected.connect(dialog.reject); form.addRow(buttons)
        if not dialog.exec(): return
        try:
            source_name=name.text().strip()
            source_url=validate_feed_url(url.text())
            if not source_name or len(source_name)>100: raise ValueError('1–100 karakterlik bir kaynak adı girin.')
            if any(row['name'].casefold()==source_name.casefold() or row['url']==source_url for row in self.source_rows): raise ValueError('Bu ad veya adres zaten kayıtlı.')
            self.db.add_source(source_name,source_url); self.refresh_sources()
        except Exception as exc:
            QMessageBox.warning(self,'Kaynak eklenemedi', str(exc))
    def remove_source(self):
        i=self.source_table.currentRow()
        if i < 0 or i >= len(self.source_rows): return
        row=self.source_rows[i]
        if row['builtin']: QMessageBox.information(self,'Kaynak','Hazır kaynaklar bu ekrandan kaldırılamaz.'); return
        self.db.remove_source(row['name']); self.refresh_sources()
    def set_auto_scan(self, checked):
        self.db.set_setting('auto_scan','1' if checked else '0')
        if hasattr(self,'timer'):
            self.timer.start() if checked else self.timer.stop()
    def start_scan(self):
        if self.scan_worker and self.scan_worker.isRunning(): return
        self.scan_messages=[]; self.scan_examined=[]; self.scan_status.setText('Kaynaklar taranıyor…'); self.scan_button.setEnabled(False)
        sources={row['name']:row['url'] for row in self.source_rows if row['scan']}
        self.scan_worker=ScanWorker(sources,self); self.scan_worker.result.connect(self.scan_result); self.scan_worker.source_error.connect(self.scan_error); self.scan_worker.finished.connect(self.scan_finished); self.scan_worker.start()
    def scan_result(self, result):
        self.scan_examined.extend(dict(item, source=result['source']) for item in result.get('examined',[]))
        try:
            added=self.db.save_scan(result['source'],result['candidates'])
            self.set_source_state(result['source'], 'Erişildi · RSS okundu')
            self.scan_messages.append(f"{result['source']}: {result['count']} kayıt incelendi, {len(result['candidates'])} olası/inceleme adayı, {added} yeni kayıt. Yalnızca RSS akışının sunduğu kayıtlar incelendi.")
        except Exception:
            self.scan_messages.append(f"{result['source']}: sonuçlar kaydedilemedi; tekrar deneyin.")
    def set_source_state(self, source, state):
        for i,row in enumerate(self.source_rows):
            if row['name']==source: self.source_table.setItem(i,2,QTableWidgetItem(state + ' · Yazma yok'))
    def scan_error(self, source, message):
        self.set_source_state(source, 'Erişilemedi')
        self.scan_messages.append(f'{source}: {message}')
    def show_scan_audit(self):
        dialog=QDialog(self); dialog.setWindowTitle('Son taramada incelenen kayıtlar'); dialog.resize(1100,650); layout=QVBoxLayout(dialog)
        note=QLabel('Yalnızca bu oturumdaki son taramanın RSS kayıtları gösterilir. Her kaynak akışının sağladığı kayıtlar ve ilk 300 öğe ile sınırlıdır.'); note.setWordWrap(True); layout.addWidget(note)
        table=QTableWidget(len(self.scan_examined),4); table.setHorizontalHeaderLabels(['KAYNAK','BAŞLIK','KARAR','GEREKÇE']); table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch); table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        for i,item in enumerate(self.scan_examined):
            for j,key in enumerate(('source','title','decision','reason')):
                table.setItem(i,j,QTableWidgetItem(item[key]))
        layout.addWidget(table)
        open_btn=QPushButton('Seçilen kaynağı tarayıcıda aç')
        def open_record():
            i=table.currentRow()
            if 0 <= i < len(self.scan_examined) and self.scan_examined[i]['url']:
                QDesktopServices.openUrl(QUrl(self.scan_examined[i]['url']))
        open_btn.clicked.connect(open_record); layout.addWidget(open_btn)
        if not self.scan_examined: note.setText('Henüz incelenmiş kayıt yok. Önce Manuel Tara düğmesine basın veya kaynak hatalarını kontrol edin.')
        dialog.exec()
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
        self.classification=QLabel(''); self.classification.setWordWrap(True); d.addWidget(self.classification)
        d.addWidget(QLabel('Talep durumu'))
        self.status=QComboBox(); self.status.addItems(['Yeni','İncelenecek','Cevap bekleniyor','Kullanıcı devraldı','Randevu','İş alındı','Tamamlandı','Uygun değil','Kapandı']); d.addWidget(self.status)
        d.addWidget(QLabel('Bu talebe ait not'))
        self.note=QTextEdit(); self.note.setPlaceholderText('Bu taleple ilgili notunuzu yazın'); d.addWidget(self.note)
        self.save_status=QLabel(''); self.save_status.setWordWrap(True); d.addWidget(self.save_status)
        save=QPushButton('Durumu ve notu kaydet'); save.setObjectName('primary'); save.clicked.connect(self.save_lead); d.addWidget(save)
        open_url=QPushButton('Kaynakta aç'); open_url.clicked.connect(self.open_source); d.addWidget(open_url); splitter.addWidget(detail); splitter.setSizes([800,400]); v.addWidget(splitter,1); return w
    def make_settings(self):
        w,v=self.page('Ayarlar','Uygulama bilgisi ve yerel veri')
        v.addWidget(QLabel(f'Talep Radarı  ·  Sürüm {self.version}  ·  Build {self.build}'))
        v.addWidget(QLabel(f'Veritabanı: {self.db.path}')); v.addWidget(QLabel('Telegram ve yerel model henüz uygulanmadı.')); v.addStretch(); return w
    def refresh(self, selected_id=None):
        # Tablo yenilenirken seçili talep kaybolmasın; kaydedilen not görünür kalsın.
        if selected_id is None and hasattr(self, 'filtered'):
            current=self.selected()
            selected_id=current['id'] if current else None
        self.rows=self.db.leads(); self.summary.setText(f'Kayıtlı talepler  {len(self.rows)}     ·     Yeni  {sum(r["status"] == "Yeni" for r in self.rows)}')
        query=self.search.text().casefold() if hasattr(self,'search') else ''
        self.filtered=[r for r in self.rows if query in ' '.join(str(r[x]) for x in ('title','source','location','description')).casefold()]
        self.table.blockSignals(True); self.table.setRowCount(len(self.filtered))
        selected_row=-1
        for i,r in enumerate(self.filtered):
            for j,key in enumerate(('id','title','source','location','status')): self.table.setItem(i,j,QTableWidgetItem(str(r[key])))
            if r['id'] == selected_id: selected_row=i
        self.table.clearSelection()
        if selected_row >= 0: self.table.selectRow(selected_row)
        else: self.table.setCurrentCell(-1,-1)
        self.table.blockSignals(False)
        if selected_row >= 0: self.show_detail()
        else:
            self.detail_title.setText('Bir talep seçin'); self.desc.clear(); self.classification.clear(); self.note.clear(); self.save_status.clear()
    def selected(self):
        i=self.table.currentRow(); return self.filtered[i] if 0 <= i < len(self.filtered) else None
    def show_detail(self):
        r=self.selected()
        if r:
            self.detail_title.setText(f'Talep #{r["id"]} · {r["title"]}'); self.desc.setText(r['description'] or 'Talep metni eklenmedi.'); self.status.setCurrentText(r['status']); self.note.setPlainText(r['note'])
            reason, explanation = classify_detail(r['title'], r['description'].split('\n\nEşleşme:',1)[0])
            self.classification.setText('⚠ ' + explanation if 'Hizmet sunma ilanı:' in explanation else '')
            self.save_status.setText('Not bu talebe kaydedildi.' if r['note'] else '')
    def add_lead(self):
        d=LeadDialog(self)
        if d.exec():
            self.db.add_lead(d.title.text(),d.source.text(),d.url.text(),d.location.text(),d.description.toPlainText()); self.refresh()
    def save_lead(self):
        r=self.selected()
        if r:
            self.db.update_lead(r['id'],self.status.currentText(),self.note.toPlainText()); self.refresh(r['id'])
            self.save_status.setText('✓ Durum ve not kaydedildi. Bu talebi seçerek tekrar görebilirsiniz.')
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
