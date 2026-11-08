# Talep Radarı (Python Masaüstü Uygulaması)

## Çalıştırma Talimatları (Geliştirme)
1. Python'ın kurulu olduğundan emin olun.
2. Bağımlılıkları yükleyin:
   `pip install -r requirements.txt`
3. Uygulamayı çalıştırın:
   `python main.py`

## Windows EXE Derleme Talimatları
Bu proje, `pyinstaller` kullanılarak EXE haline getirilebilir. Bu işlem AI Studio ortamında yapılamaz.

1. Windows makinenizde sanal ortam oluşturun:
   `python -m venv venv`
   `venv\Scripts\activate`
2. Gereksinimleri yükleyin:
   `pip install -r requirements.txt pyinstaller`
3. EXE oluşturun:
   `pyinstaller --noconsole --onefile --name "TalepRadari" main.py`

*`dist/` klasörü içerisinde `TalepRadari.exe` oluşacaktır.*
