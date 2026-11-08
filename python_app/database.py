import sqlite3
from pathlib import Path
import os

# Kullanıcı verileri uygulama klasöründen bağımsız saklanır.
def database_path():
    root = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'TalepRadari'
    root.mkdir(parents=True, exist_ok=True)
    return root / 'radar.sqlite'

class Database:
    def __init__(self, path=None):
        self.path = str(path or database_path())
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''
            CREATE TABLE IF NOT EXISTS leads (
              id INTEGER PRIMARY KEY, title TEXT NOT NULL, source TEXT NOT NULL DEFAULT '',
              url TEXT NOT NULL DEFAULT '', location TEXT NOT NULL DEFAULT '',
              description TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'Yeni',
              note TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            ''')
    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        return db
    def add_lead(self, title, source, url, location, description):
        if not title.strip(): raise ValueError('Başlık gerekli')
        with self.connect() as db:
            db.execute('INSERT INTO leads(title,source,url,location,description) VALUES(?,?,?,?,?)',
                       (title.strip(), source.strip(), url.strip(), location.strip(), description.strip()))
    def leads(self):
        with self.connect() as db: return [dict(r) for r in db.execute('SELECT * FROM leads ORDER BY id DESC')]
    def update_lead(self, lead_id, status, note):
        with self.connect() as db: db.execute('UPDATE leads SET status=?,note=? WHERE id=?', (status, note, lead_id))
    def get_setting(self, key, default=''):
        with self.connect() as db:
            row = db.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
            return row[0] if row else default
    def set_setting(self, key, value):
        with self.connect() as db:
            db.execute('INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key,value))
