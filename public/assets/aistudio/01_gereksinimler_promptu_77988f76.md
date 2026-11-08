# Talep Radarı — Bilgisayar sürümü / Gereksinimler promptu

Tarih: 8 Kasım 2026 · Sürüm: 1.0

Kullanım: Aşağıdaki bloğu geliştirme aracına yapıştır. Üreteceği gereksinim belgesini, ikinci ve üçüncü promptla birlikte kullan. Bu dosya bir prompttur; uygulama veya tamamlanmış entegrasyon değildir.

```text
Kıdemli ürün analisti ve masaüstü yazılım ürün sahibi olarak çalış. Talep Radarı adlı Windows öncelikli masaüstü uygulaması için, geliştiricinin doğrudan kullanabileceği ayrıntılı ve test edilebilir gereksinim analizi üret. Genel fikir listesiyle yetinme; numaralandırılmış gereksinimler, durum geçişleri, hata senaryoları ve kabul kriterleri yaz. Belirsiz entegrasyonu çalışıyor gibi sunma. Rutin kararlar için tekrar onay isteme; varsayımları açıkça belirt.

ÜRÜN AMACI
Kullanıcı ve eşi 08.00–17.00 çalışıyor; akşam ve hafta sonu bilgisayar bakım, SSD/RAM yükseltme, kurulum ve basit teknik destek işi alabilecekler. Uygulama seçilmiş internet kaynaklarında hizmet arayanları bulacak, uygun taleplere ilk cevap hazırlayacak, desteklenen kaynaklarda gönderecek, dönüşleri Telegram'a aktaracak. Kullanıcı Telegram'dan cevaplayınca program mesajı asıl kaynaktaki aynı konuşmaya iletecek. Sonraki müşteri mesajları yine Telegram'a gelecek. Otomatik satış kapatma, ödeme alma veya fiyat pazarlığı yapmayacak.

TEMEL KARARLAR
- Önce bilgisayar sürümü. APK, mobil uygulama ve sunucu bu sürümün teslimi değildir.
- Mevcut XMusic, XIPTV ve XFiles projelerinden bağımsız ürün.
- Windows 11 x64 öncelikli; arayüz Türkçe. Kod ve tanımlayıcılar İngilizce; açıklamalar ve kod yorumları Türkçe.
- Ücretli yapay zekâ API'si, abonelik, ücretli sunucu veya Firebase zorunlu değil. Mevcut bilgisayar ve internet kullanılır; elektrik ve internet tüketimi sıfır sayılmaz.
- Bildirim ve uzaktan sohbet Telegram botuyla. WhatsApp ilk sürümde zorunlu değil.
- Asıl müşteri görüşmesi kaynakta kalır; Telegram kullanıcı için bir köprüdür. Müşterinin Telegram kullanması gerekmez.
- Yalnızca okuma, gönderme ve takip yetenekleri test edilmiş kaynaklarda tam köprü etkin olur. Diğerlerinde taslak ve “Kaynağı aç” bulunur.
- Bilgisayar açık, uyanık ve internete bağlıyken motor çalışır. Kapalıyken tarama veya Telegram üzerinden gönderim garanti edilmez.
- Kaynakların kapalı alanlarına erişim uydurulmaz; CAPTCHA veya erişim engelinde kaynak duraklatılır. Hukuk/vergi raporu bu çalışmanın kapsamı değildir.

KAYNAK KAPSAMI
Başlangıç araştırma adayları: Technopat Sosyal, Techolay Sosyal, DonanımHaber Forum, Donanım Arşivi Forum, ShiftDelete.Net Forum ve R10. Bunların okuma, yazma, RSS ve özel mesaj erişimleri henüz entegrasyon testiyle doğrulanmış değildir. Google Alerts yardımcı keşif kaynağı; eksiksiz veya canlı tarama değildir. Bluesky isteğe bağlı açık API pilotudur; yerel talep hacmi ölçülür.
Discord ve Telegram yalnızca erişim sağlanan sunucu/grup/kanallarda eklenir. WhatsApp, Facebook grupları, Instagram, Threads, X, Reddit ve benzerleri başlangıçta çalışan kaynak olarak gösterilmez; mevcut erişim, maliyet ve yöntem doğrulanınca ayrı adaptör kapsamına alınır.
Sistemin “bütün interneti tarama” vaadi olmayacak. İzlenen kaynaklar ve gerçek kapsama aralıkları görülebilecek.

KULLANICI AKIŞI
1. Hizmetler, ilçeler, müsaitlik, fiyat kuralları ve sessiz saatler tanımlanır.
2. Telegram botu oluşturma/bağlama adımları uygulanır. Token güvenli saklanır; yetkili Telegram user ID ve chat ID doğrulanır.
3. Kaynak eklenir, bağlantı testi yapılır ve gerçek yetenekler gösterilir.
4. Zamanlanmış veya manuel tarama yeni kayıtları toplar; normalize eder, tekrarları eler.
5. Kurallar açık hizmet niyeti, hizmet uyumu, konum ve güncelliğe göre adayları ayırır.
6. Küçük yerel model yalnızca uygun adayları yorumlar ve izinli şablonlardan cevap hazırlar. Model yoksa şablonlarla devam edilir.
7. Başlangıçta Telegram veya masaüstünde “Gönder / Düzenle / Geç” onayı istenir. Kaynak bazlı otomatik ilk cevap kullanıcı tarafından ayrıca etkinleştirilebilir.
8. Doğrulanmış gönderimin harici mesaj kimliği ve kaynak bağlantısı saklanır.
9. Müşteri dönüşü Telegram'a talep numarası ve konuşma bağlamıyla iletilir.
10. Kullanıcının Telegram yanıtı yalnızca eşleştirildiği konuşmaya gönderilir.
11. Kullanıcı devralınca otomatik cevaplar ve henüz gönderilmemiş model mesajları iptal edilir. Model yalnızca kullanıcıya taslak önerir.
12. Görüşme randevu, iş alındı, tamamlandı, vazgeçti veya kapandı olarak işaretlenir.

AYRINTILANDIRILACAK GEREKSİNİMLER
R01 Profil: İstanbul'un 39 ilçesi, seçilebilir öncelikli ilçeler, Anadolu/Avrupa yakası, hizmet saatleri, yerinde/teslim hizmet seçimi. Kullanıcının ikamet ilçesini uydurma. Metinde konum yoksa “Konum sorulacak”; profil konumu ile işin konumu ayrı. Semt-ilçe eşleştirmesindeki belirsizlik korunur.
R02 Niyet: “SSD takacak biri lazım” güçlü; “SSD önerir misiniz?” bilgi sorusu; “SSD satıyorum” hizmet talebi değil. Olumsuzluk, çözülmüş ihtiyaç, eski alıntı, servis reklamı ve tekrar gönderileri ele al. Kural puanı gerçek olasılık veya doğruluk yüzdesi değildir.
R03 Kaynak yetenekleri: discovery/read/threadFollow/directMessageRead/sendReply/sendAttachment/reactionEvents ayrı alanlar. Açık konu okuyabilmek özel mesaj okuyabilmek anlamına gelmez.
R04 Tekrarlar: Kaynak+harici kayıt kimliği; eksikse normalize URL+özet. Aynı ilk cevap bir kez. Siteler arası benzerlik otomatik kişi birleştirme yapmaz.
R05 İlk cevap: Kısa, dürüst, hizmete uygun. Bilinmeyen cihaz modeli/ilçe sorulur. Kullanıcı tarafından tanımlanmamış fiyat, kesin arıza, stok veya randevu vaat edilmez. Tahmini fiyat ile bağlayıcı teklif ayrılır. Model kendiliğinden iletişim bilgisi üretmez.
R06 Telegram köprüsü: Tek yetkili kullanıcı varsayılan; eş erişimi ayrıca açıkça eklenebilir. User ID ve chat ID allowlist zorunlu. Müşteri başına ayrı konu desteklenen forum özellikli Telegram grubunda kullanılabilir; alternatif özel sohbette talep numarası + Reply eşleştirmesi. İki yöntem için yanlış yönlendirme önlenir. Yeni Telegram grubunun kendiliğinden oluşturulabileceğini varsayma.
R07 Yönlendirme: Telegram reply mesajı/topic ID ile kaynak konuşması kesin eşleşmeli. Eşleşme yoksa gönderim yapılmaz; hedef seçimi ve önizleme istenir. Yerel mesaj harici gönderimi doğrulanmadan “Gönderildi” denmez.
R08 Devralma: Kullanıcı devralması kalıcı kilit oluşturur. İlk manuel yanıtta da devralma gerçekleşir. Gönderici son anda sahiplik ve izinleri yeniden kontrol eder. Yetkili iki kişinin çakışan işlemleri ele alınır.
R09 Dönüşler: Doğrudan yanıt, alıntı, özel mesaj, genel konu hareketi ve emoji tepkisi ayrı sınıflar. Kaynak desteklemiyorsa algılandığı iddia edilmez. Varsayılan kritik bildirim doğrudan müşteri yanıtıdır.
R10 Dosyalar: Desteklenen kaynaklarda resim/dosya köprüsü. Boyut/tür limitleri, güvenli önizleme, indirme hatası, desteklenmeyen ek için bağlantı/metin alternatifi. Gelen dosya otomatik çalıştırılmaz.
R11 Güvenilirlik: Kalıcı gönderim kuyruğu, tekrar engeli, hız sınırı, geçici hata beklemesi, token süresi dolması ve belirsiz gönderim yönetimi. Zaman aşımı sonrasında kör tekrar yok. Telegram'a aynı olayın tekrar tekrar aktarımı engellenir.
R12 Çevrimdışı: Bekleyen gönderim sayısı ve yaşı görünür. Yeniden açılışta eski müşteri adayına otomatik ilk cevap gönderilmez; tazelik yeniden değerlendirilir. Eski manuel mesajlar yaş sınırını aştıysa yeniden onay ister.
R13 Kontroller: Tarama duraklatma ve tüm gönderimleri durdurma ayrı. Acil durdurma kalıcıdır, yeniden açılışta kendiliğinden kalkmaz. Sessiz saatler ve günlük kaynak limitleri kullanıcı ayarıdır; platform limiti diye sunulmaz.
R14 Takip: Yeni, incelenecek, ilk cevap onayında, cevap bekleniyor, kullanıcı devraldı, randevu, iş alındı, tamamlandı, uygun değil, kapandı. Mesaj teslim durumu ayrı bir durum kümesidir.
R15 Rapor: Varsayılan hedef 20.30 Europe/Istanbul, değiştirilebilir. Yeni uygun talepler, gönderimler, müşteri dönüşleri, sonuçlanan işler, hatalı kaynaklar, kapsam boşlukları. Kaynak bazlı gerçek verim: uygun işaretlenen talep, dönüş ve alınan iş. Kaynak hatası “talep yok” sayılmaz.
R16 Yerel model: İsteğe bağlı, tek görev eşzamanlı, kuyruk sınırı, kısa bağlam ve çıktı sınırı. Model hatası tarama/Telegram aktarımını durdurmaz. İnternet içeriği ve müşteri mesajları model için veri; uygulama talimatı veya araç yetkisi değildir.
R17 Güvenlik: Token/parola loga ve Telegram hata metnine yazılmaz. Kaynak oturumları güvenli saklanır. Bot komutlarını yalnızca yetkili kişiler çalıştırır. Model tokenlara, kabuğa ve araçlara erişmez. Yerel panel varsayılan internete açılmaz.
R18 Veri: Yerel SQLite, veri kaybetmeyen güncelleme, yedekleme/geri yükleme, saklama süreleri, notlar, CSV/metin dışa aktarma. Yedeklerde sırlar bulunmaz. Sürüm/yapı numarası ve tanılama ekranı.

KABUL TESTLERİ
- Aynı kaynak üç kez tarandığında tek talep ve en fazla bir ilk cevap.
- Kullanıcı Reply ile A müşterisini yanıtlarken B müşterisine mesaj gitmemesi.
- Yetkisiz Telegram kullanıcısının komut/mesaj gönderememesi.
- Devralma ile aynı anda biten model cevabının otomatik gönderilmemesi.
- Ağ zaman aşımı sonrası çift mesaj oluşmaması veya sonuç belirsizse güvenli duraklama.
- Bilgisayar yeniden başlatıldığında eşleşmeler, sahiplik ve acil durdurma korunması.
- Model çalışmazken tarama, şablon, gelen mesaj ve manuel yanıtın çalışması.
- Yalnızca okunan kaynakta gönder düğmesinin gönderim yapıyormuş gibi davranmaması.
- Test verisi, gerçek müşteri ve gerçek gönderimlerin açıkça ayrılması.

ÇIKTI FORMATI
1. Amaç, kapsam ve kapsam dışı.
2. Kullanıcı senaryoları ve uçtan uca akış.
3. ID, öncelik, tetikleyici, davranış, hata ve kabul kriteri içeren gereksinim tablosu.
4. Talep, mesaj ve görüşme sahipliği için ayrı durum geçiş tabloları.
5. Kaynak yetenek matrisi: doğrulanmış / test edilecek / desteklenmiyor.
6. Fonksiyonel olmayan gereksinimler ve ölçülebilir performans hedefleri.
7. MVP ve sonraki sürümler; kaynak erişimine bağlı engeller.
8. Varsayımlar ve yalnızca gerçekten cevap gerektiren açık sorular.

İlk sürümün başarı ölçütü: en az bir kaynakta keşiften Telegram üzerinden karşılıklı mesajlaşmaya kadar gerçek ve doğrulanmış zincir. Kamu forumunda yazma erişimi yoksa bunu gizleme; kontrollü test kaynağıyla köprüyü, gerçek forumla okuma pilotunu ayrı raporla. Bu promptta belge üret; çalıştırmadığın kodu veya entegrasyonu tamamlandı diye sunma.
```
