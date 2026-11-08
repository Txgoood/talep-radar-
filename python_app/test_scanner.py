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
    def test_turkish_candidate_classification(self):
        from scanner import classify
        self.assertIn('Olası hizmet talebi', classify('Kadıköy bilgisayar tamiri için usta arıyorum', ''))
        self.assertIn('İncelenecek aday', classify('Laptop termal macun yenileme', ''))
        self.assertIsNone(classify('Hangi SSD önerirsiniz?', ''))
        self.assertIsNone(classify('SSD satıyorum', ''))
        self.assertIsNone(classify('SSD servisi aramıyorum', ''))
        self.assertIsNone(classify('Sıvı soğutma önerisi', 'Hangisini alayım?'))
    def test_atom_and_invalid(self):
        self.assertEqual(len(parse_feed(ATOM)[1]),1)
        with self.assertRaises(ScanError): parse_feed(b'<html>blocked</html>')
        with self.assertRaises(ScanError): parse_feed(b'<!DOCTYPE a [<!ENTITY x SYSTEM "file:///x">]><rss/>')
    def test_http_failure_not_empty_success(self):
        error=HTTPError('https://example.com',403,'blocked',{},None)
        with patch('urllib.request.urlopen', side_effect=error):
            with self.assertRaisesRegex(ScanError,'403'): fetch_feed('Techolay Sosyal')

if __name__ == '__main__': unittest.main()
