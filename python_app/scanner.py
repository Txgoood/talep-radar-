"""Herkese açık RSS akışları için sınırlı, salt okunur keşif."""
import html
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlsplit

SOURCES = {
    'Techolay Sosyal': 'https://techolay.net/sosyal/bolum/-/index.rss',
    'Technopat Sosyal': 'https://www.technopat.net/sosyal/bolum/-/index.rss',
}
MAX_BYTES = 2_000_000

class ScanError(Exception):
    pass

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.parts = []
    def handle_data(self, text):
        self.parts.append(text)

def plain_text(value):
    parser = TextExtractor(); parser.feed(value or '')
    return re.sub(r'\s+', ' ', ' '.join(parser.parts)).strip()[:6000]

def classify(title, description):
    text = (title + ' ' + description).lower().replace('ı','i')
    # Bir bilgi sorusunu iş talebi olarak göstermemek için iki kanıt aranır.
    if any(x in text for x in ('satiyorum', 'satilik', 'satıyorum', 'alınır satılır', 'öneri', 'oneri', 'hangisini al')):
        return None
    service = next((x for x in ('ssd', 'ram', 'termal macun', 'format', 'bilgisayar tamir', 'laptop tamir', 'montaj', 'yükseltme', 'yukseltme') if x in text), None)
    intent = next((x for x in ('usta', 'servis', 'yapacak', 'takacak', 'yardimci olacak', 'yardımcı olacak', 'yaptirmak', 'yaptırmak', 'arıyorum', 'ariyorum', 'arıyom', 'ihtiyacim var', 'ihtiyacım var', 'nerede yaptir', 'nerede yaptır') if x in text), None)
    if not service or not intent: return None
    return f'Hizmet ifadesi: {service}; talep ifadesi: {intent}. Konum doğrulanmalı.'

def parse_feed(data):
    if len(data) > MAX_BYTES: raise ScanError('Akış boyutu güvenlik sınırını aştı.')
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper(): raise ScanError('Akışta desteklenmeyen XML bildirimi var.')
    try: root = ET.fromstring(data)
    except ET.ParseError as exc: raise ScanError('Kaynak RSS/Atom verisi göndermedi.') from exc
    entries = root.findall('.//item')
    atom = '{http://www.w3.org/2005/Atom}'
    if not entries: entries = root.findall('.//' + atom + 'entry')
    if root.tag not in ('rss', 'rdf', '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF', atom+'feed'):
        raise ScanError('Yanıt geçerli bir RSS/Atom akışı değil.')
    found = []
    for entry in entries[:300]:
        title = plain_text(entry.findtext('title') or entry.findtext(atom+'title') or '')
        desc = plain_text(entry.findtext('description') or entry.findtext(atom+'summary') or entry.findtext(atom+'content') or '')
        link = (entry.findtext('link') or '').strip()
        if not link:
            el = entry.find(atom+'link'); link = el.get('href','').strip() if el is not None else ''
        parsed = urlsplit(link)
        if parsed.scheme not in ('http','https') or not parsed.hostname or not title: continue
        reason = classify(title,desc)
        if reason: found.append({'title':title[:500], 'description':desc, 'url':link[:2048], 'reason':reason})
    return len(entries), found

def fetch_feed(name, timeout=15):
    url = SOURCES[name]
    request = urllib.request.Request(url, headers={'User-Agent':'TalepRadari/0.2 (RSS reader)', 'Accept':'application/rss+xml, application/atom+xml, application/xml, text/xml'})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data=response.read(MAX_BYTES+1)
    except urllib.error.HTTPError as exc:
        if exc.code == 429: raise ScanError('429 hız sınırı; kaynak daha sonra tekrar denenmeli.') from exc
        if exc.code in (401,403): raise ScanError(f'HTTP {exc.code}: kaynak erişimi engelledi veya oturum gerektiriyor.') from exc
        raise ScanError(f'HTTP {exc.code}: akışa erişilemedi.') from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise ScanError('Bağlantı başarısız veya zaman aşımına uğradı.') from exc
    count, candidates = parse_feed(data)
    return {'source':name,'count':count,'candidates':candidates}
