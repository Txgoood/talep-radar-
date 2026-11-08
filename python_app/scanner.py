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
    'Techolay Teknik Destek': 'https://techolay.net/sosyal/bolum/teknik-destek.10/index.rss',
    'Technopat Teknik Destek': 'https://www.technopat.net/sosyal/bolum/teknik-destek.230/index.rss',
    'Technopat Hizmet İlanları': 'https://www.technopat.net/sosyal/bolum/hizmet-ilanlari.148/index.rss',
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

def normalize(value):
    # Türkçe büyük/küçük I ve yaygın Türkçe karakter varyantları karşılaştırılır.
    text = value.translate(str.maketrans({'İ':'i','I':'ı'})).lower()
    return text.translate(str.maketrans({'ı':'i','ş':'s','ğ':'g','ü':'u','ö':'o','ç':'c'}))

def classify_detail(title, description):
    text = normalize(title + ' ' + description)
    services = ('ssd', 'ram', 'termal macun', 'format', 'bilgisayar', 'laptop',
                'dizustu', 'masaustu', 'pc', 'anakart', 'ekran karti', 'sivi sogutma')
    service = next((word for word in services if re.search(r'(?<!\w)' + re.escape(word) + r'(?!\w)', text)), None)
    if not service: return None, 'Bilgisayar veya hizmet anahtar ifadesi bulunamadı.'
    # Ücretli hizmet sunan ilanları müşteri talebi gibi işaretleme.
    offers = (r'hizmet\s+(?:verilir|veriyorum|vermekteyim|verebilirim|sunulur|sunuyorum)',
              r'(?:hizmeti|hizmetleri)\s+(?:verilir|veriyorum|sunulur)',
              r'(?:montaj|tamir|bakim|format|kurulum)\s+(?:hizmeti\s+)?(?:yapilir|yapiyorum|yapmaktayim)',
              r'(?:verebilecegim|sundugum|verdigim)\s+hizmetler',
              r'(?:yardimci|destek)\s+olurum', r'(?:montaj|tamir|bakim)\s+yapilir')
    offered = next((m.group(0) for pattern in offers if (m := re.search(pattern, text))), None)
    if offered:
        return None, f'Hizmet sunma ilanı: {offered}. Müşteri talebi olarak değerlendirilmedi.'
    exclusions = ('satiyorum', 'satilik', 'alınır satılır', 'cozuldu', 'sorun cozuldu', 'servis aramiyorum', 'usta aramiyorum')
    exclusion = next((x for x in exclusions if normalize(x) in text), None)
    if exclusion: return None, f'Dışlama ifadesi: {exclusion}'
    strong = ('usta', 'teknisyen', 'servis ariyorum', 'tamirci', 'takacak', 'montaj yapacak',
              'yapacak birini', 'yaptirmak', 'yapabilecek', 'takabilecek', 'yardimci olacak',
              'nerede yaptir', 'servise gotur', 'tamir ettir', 'is yaptirmak istiyorum')
    intent = next((word for word in strong if word in text), None)
    if intent:
        reason = f'Olası hizmet talebi · cihaz/iş: {service}; ifade: {intent}. Konum ve ihtiyaç doğrulanmalı.'
        return reason, reason
    # Açık arıza veya montaj ifadelerini kullanıcı değerlendirmesi için ayrıca sakla.
    review = ('tamir', 'onarim', 'montaj', 'kurulum', 'format at', 'ssd tak', 'ram tak',
              'ssd degis', 'ram degis', 'ekran degis', 'termal macun', 'bakim yap', 'arizali')
    hint = next((word for word in review if word in text), None)
    if hint:
        reason = f'İncelenecek aday · cihaz/iş: {service}; ifade: {hint}. İş talebi ve konum doğrulanmadı.'
        return reason, reason
    return None, f'İlgili ifade: {service}; hizmet talebi veya bakım/montaj ifadesi bulunamadı.'

def classify(title, description):
    return classify_detail(title, description)[0]

def parse_feed_details(data):
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
    examined = []
    for entry in entries[:300]:
        title = plain_text(entry.findtext('title') or entry.findtext(atom+'title') or '')
        desc = plain_text(entry.findtext('description') or entry.findtext(atom+'summary') or entry.findtext(atom+'content') or '')
        link = (entry.findtext('link') or '').strip()
        if not link:
            el = entry.find(atom+'link'); link = el.get('href','').strip() if el is not None else ''
        parsed = urlsplit(link)
        if parsed.scheme not in ('http','https') or not parsed.hostname or not title:
            examined.append({'title': title or '(Başlık yok)', 'url': '', 'decision': 'Elenmiş', 'reason': 'Eksik başlık veya geçersiz bağlantı.'}); continue
        reason, explanation = classify_detail(title,desc)
        examined.append({'title':title[:500], 'url':link[:2048], 'decision':'Aday' if reason else 'Elenmiş', 'reason':explanation})
        if reason: found.append({'title':title[:500], 'description':desc, 'url':link[:2048], 'reason':reason})
    return len(entries), found, examined

def parse_feed(data):
    count, found, _ = parse_feed_details(data)
    return count, found

def validate_feed_url(url):
    parsed = urlsplit(url.strip())
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise ValueError('Kullanıcı bilgisi içermeyen geçerli bir HTTPS RSS adresi girin.')
    # Özel adresler veritabanında saklandığından sır içeren parametreleri kabul etme.
    if re.search(r'(?i)(?:^|[?&])(token|password|secret|key|api_key|access_token)=', parsed.query):
        raise ValueError('Gizli anahtar içeren adresler eklenemez.')
    return url.strip()

def fetch_feed(name, timeout=15, url=None):
    url = validate_feed_url(url or SOURCES[name])
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
    total, candidates, examined = parse_feed_details(data)
    return {'source':name,'count':len(examined),'total':total,'candidates':candidates,'examined':examined}

class FeedLinks(HTMLParser):
    # Sayfanın yalnızca açıkça ilan ettiği RSS/Atom adreslerini inceler.
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        if tag.lower() != 'link': return
        item=dict(attrs)
        rel=(item.get('rel') or '').lower().split()
        kind=(item.get('type') or '').lower().split(';')[0].strip()
        if 'alternate' in rel and kind in ('application/rss+xml','application/atom+xml') and item.get('href'):
            self.links.append(item['href'])

def discover_feed_url(site_url):
    from urllib.parse import urljoin
    site_url=validate_feed_url(site_url)
    host=(urlsplit(site_url).hostname or '').lower().removeprefix('www.')
    request=urllib.request.Request(site_url,headers={'User-Agent':'TalepRadari/0.5 (RSS reader)','Accept':'text/html,application/rss+xml,application/atom+xml,application/xml'})
    try:
        with urllib.request.urlopen(request,timeout=15) as response:
            final_url=response.geturl()
            final_host=(urlsplit(final_url).hostname or '').lower().removeprefix('www.')
            if final_host != host: raise ScanError('Site başka bir alana yönlendirdi; otomatik keşif durduruldu.')
            data=response.read(MAX_BYTES+1)
    except urllib.error.HTTPError as exc:
        if exc.code in (401,403,429): raise ScanError(f'HTTP {exc.code}: erişim engellendi veya sınırlandı.') from exc
        raise ScanError(f'HTTP {exc.code}: siteye ulaşılamadı.') from exc
    except (urllib.error.URLError,TimeoutError,OSError) as exc:
        raise ScanError('Siteye bağlanılamadı veya zaman aşımı oluştu.') from exc
    if len(data)>MAX_BYTES: raise ScanError('Site yanıtı boyut sınırını aştı.')
    try:
        parse_feed_details(data)
        return validate_feed_url(final_url)
    except ScanError:
        pass
    parser=FeedLinks(); parser.feed(data.decode('utf-8',errors='replace'))
    for href in parser.links[:3]:
        candidate=urljoin(final_url,href)
        try:
            candidate=validate_feed_url(candidate)
            if (urlsplit(candidate).hostname or '').lower().removeprefix('www.') != host: continue
            fetch_feed('Keşif',url=candidate)
            return candidate
        except (ValueError,ScanError): continue
    raise ScanError('Sitede erişilebilen açık RSS/Atom akışı bulunamadı; otomatik tarama etkinleştirilmedi.')
