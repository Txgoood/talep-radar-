import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from database import Database
from scanner import parse_feed, fetch_feed, ScanError

RSS = b'''<?xml version="1.0"?><rss version="2.0"><channel>
<item><title>Kartal SSD takacak usta ariyorum</title><link>https://example.com/1</link><description>Montaj yaptirmak istiyorum</description></item>
<item><title>Hangi SSD onerirsiniz?</title><link>https://example.com/2</link><description>Bilgi</description></item>
</channel></rss>'''
ATOM = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>RAM takacak usta ariyorum</title><link href="https://example.com/a"/><summary>Test</summary></entry></feed>'''

class ScannerTest(unittest.TestCase):
    def test_feed_and_dedup(self):
        count, results = parse_feed(RSS)
        self.assertEqual(count, 2); self.assertEqual(len(results), 1)
        with tempfile.TemporaryDirectory() as directory:
            db = Database(Path(directory)/'test.db')
            self.assertEqual(db.save_scan('Test',results),1)
            self.assertEqual(db.save_scan('Test',results),0)
            self.assertEqual(len(db.leads()),1)
            self.assertEqual(db.leads()[0]['location'],'Konum doğrulanmalı')
    def test_audit_shows_candidates_and_rejections(self):
        from scanner import parse_feed_details
        total, candidates, examined = parse_feed_details(RSS)
        self.assertEqual(total, 2)
        self.assertEqual(len(examined), 2)
        self.assertEqual([x['decision'] for x in examined], ['Aday', 'Elenmiş'])
        self.assertTrue(examined[1]['reason'])
        self.assertEqual(len(candidates), 1)
    def test_catalog_is_not_mistaken_for_scannable_feeds(self):
        from source_catalog import CATALOG
        from scanner import SOURCES
        self.assertGreater(len(CATALOG), 30)
        self.assertTrue(all(name not in SOURCES for name, _, _ in CATALOG))
    def test_site_rss_discovery_and_validation(self):
        from scanner import discover_feed_url, ScanError
        from io import BytesIO
        class Response(BytesIO):
            def geturl(self): return 'https://example.com/forum/'
        page = b'<html><head><link rel="alternate" type="application/rss+xml" href="/feed.xml"></head></html>'
        with patch('urllib.request.urlopen', return_value=Response(page)):
            with patch('scanner.fetch_feed', return_value={'count': 1, 'candidates': []}) as probe:
                self.assertEqual(discover_feed_url('https://example.com/forum/'), 'https://example.com/feed.xml')
                probe.assert_called_once()
        with patch('urllib.request.urlopen', return_value=Response(b'<html>no feed</html>')):
            with self.assertRaisesRegex(ScanError, 'bulunamadı'): discover_feed_url('https://example.com/forum/')
    def test_discovery_rejects_external_feed(self):
        from scanner import discover_feed_url, ScanError
        from io import BytesIO
        class Response(BytesIO):
            def geturl(self): return 'https://example.com/'
        page=b'<link rel="alternate" type="application/rss+xml" href="https://other.example/rss">'
        with patch('urllib.request.urlopen',return_value=Response(page)):
            with self.assertRaises(ScanError): discover_feed_url('https://example.com/')
    def test_custom_sources_and_url_validation(self):
        from scanner import validate_feed_url
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'source.db'
            db = Database(path)
            db.add_source('Test RSS', validate_feed_url('https://example.com/feed'))
            self.assertEqual(Database(path).custom_sources()[0]['name'], 'Test RSS')
            db.remove_source('Test RSS')
            self.assertEqual(db.custom_sources(), [])
        for unsafe in ('http://example.com/rss', 'https://u:password@example.com/feed', 'https://example.com/feed?token=secret'):
            with self.assertRaises(ValueError): validate_feed_url(unsafe)
    def test_cross_feed_dedup(self):
        _, items = parse_feed(RSS)
        with tempfile.TemporaryDirectory() as directory:
            db=Database(Path(directory)/'test.db')
            self.assertEqual(db.save_scan('Genel',items),1)
            self.assertEqual(db.save_scan('Teknik Destek',items),0)
    def test_turkish_candidate_classification(self):
        from scanner import classify
        self.assertIn('Olası hizmet talebi', classify('Kadıköy bilgisayar tamiri için usta arıyorum', ''))
        self.assertIn('İncelenecek aday', classify('Laptop termal macun yenileme', ''))
        self.assertIsNone(classify('Hangi SSD önerirsiniz?', ''))
        self.assertIsNone(classify('SSD satıyorum', ''))
        self.assertIsNone(classify('SSD servisi aramıyorum', ''))
        self.assertIsNone(classify('Sıvı soğutma önerisi', 'Hangisini alayım?'))
    def test_service_provider_is_not_a_customer(self):
        from scanner import classify_detail
        title = "Ankara'da masaüstü bilgisayar toplama ve montaj hizmeti verilir"
        body = "Ücreti karşılığında montajında yardımcı olurum. Verebileceğim hizmetler: SSD ve RAM montajı."
        result, reason = classify_detail(title, body)
        self.assertIsNone(result)
        self.assertIn('Hizmet sunma ilanı', reason)
        self.assertIsNotNone(classify_detail('Kadıköy SSD takacak usta arıyorum', '')[0])
        self.assertIsNotNone(classify_detail('Laptop tamir ettirmek istiyorum', 'Ücret karşılığı yardım arıyorum')[0])
    def test_atom_and_invalid(self):
        self.assertEqual(len(parse_feed(ATOM)[1]),1)
        with self.assertRaises(ScanError): parse_feed(b'<html>blocked</html>')
        with self.assertRaises(ScanError): parse_feed(b'<!DOCTYPE a [<!ENTITY x SYSTEM "file:///x">]><rss/>')
    def test_http_failure_not_empty_success(self):
        error=HTTPError('https://example.com',403,'blocked',{},None)
        with patch('urllib.request.urlopen', side_effect=error):
            with self.assertRaisesRegex(ScanError,'403'): fetch_feed('Techolay Sosyal')

if __name__ == '__main__': unittest.main()
