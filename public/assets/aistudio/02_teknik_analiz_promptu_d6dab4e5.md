# Talep Radarı — Bilgisayar sürümü / Teknik analiz promptu

Tarih: 8 Kasım 2026 · Sürüm: 1.0

Kullanım: 01 numaralı prompttan çıkan gereksinim belgesini ekle; ardından aşağıdaki bloğu yapıştır. Tasarım dosyası da hazırsa onu da bağlam olarak ekle. Bu prompt mimari ve uygulanabilir geliştirme planı içindir; derleme yapılmış olduğu anlamına gelmez.

```text
Kıdemli masaüstü yazılım mimarı ve entegrasyon mühendisi olarak çalış. Ekli gereksinimleri Talep Radarı adlı Windows öncelikli uygulama için ayrıntılı teknik analize dönüştür. Kodlama kararlarını, veri modelini, mesaj sözleşmelerini, yarış koşullarını, testleri ve teslim aşamalarını somutlaştır. Örnek kodlarla yetinip çalışan ürün iddiasında bulunma. Bu aşamada önce teknik analiz belgesini üret; tam uygulama geliştirmesi ayrı adımdır.

SABİT ÜRÜN AKIŞI
Seçilmiş kaynaklarda hizmet talebi keşfi → kurallarla eleme → küçük yerel model veya şablonla ilk cevap → başlangıçta kullanıcı onayı, sonradan kaynak bazlı otomatik ilk cevap → kaynakta doğrulanmış gönderim → müşteri yanıtını Telegram'a aktarma → kullanıcının Telegram cevabını aynı kaynak konuşmasına iletme. Kullanıcı devralınca otomatik yanıt durur. Telegram'a bildirim düşmesi, sohbetin Telegram'a taşındığı anlamına gelmez. Tam köprü sadece gerçek okuma/yazma/takip erişimi olan kaynaklarda çalışır.

TEKNOLOJİ BAŞLANGIÇ KARARI
- Python 3.12 veya geliştirme tarihinde uyumlu kararlı bir Python sürümü, PySide6/Qt Widgets masaüstü arayüzü, SQLite yerel veritabanı.
- UI thread üzerinde ağ, tarama, model çıkarımı veya uzun DB işi çalışmaz.
- Arayüz + ayrı worker süreci veya eşdeğer net yaşam döngüsü olan motor. Yerel model ayrı süreç; tek seferde bir üretim. İlk sürüm için dağıtık mikroservis kurma.
- Asenkron HTTP istemcisi, HTML ayrıştırıcı, Telegram Bot API istemcisi, sürümlü migration ve şema doğrulama katmanı. Bağımlılık sürümlerini uygulama geliştirmesinde resmî belgelerden doğrula ve kilitle; uyumluluk uydurma.
- Standart okuma için HTTP/API/RSS öncelikli. Tarayıcı zorunluysa isteğe bağlı Playwright adaptörü; bütün kaynaklarda sürekli tarayıcı açık tutma.
- Yerel model için llama.cpp uyumlu GGUF ve localhost üzerinden sınırlı bir istemci öner. Ollama mevcutsa alternatif bağlantı olabilir; ikisini birden zorunlu kurdurma. Uygulama model olmadan çalışabilsin.
- Model adını ezbere kesinleştirme: lisansı ve Türkçe başarımı doğrulanan yaklaşık 1.5B–4B sınıfında Q4 model adaylarını küçük bir veri kümesiyle karşılaştır. Boyut tek başına kalite veya RAM garantisi değildir. CPU varsayılan, GPU isteğe bağlı.
- İlk hedef Windows 11 x64. Kod İngilizce, kullanıcı metinleri ve açıklamalar Türkçe. Android APK, ücretli bulut, Firebase ve çalışma sırasında ücretli LLM API'si zorunlu değil.

MODÜLLERİ VE ARAYÜZLERİ TASARLA
SourceRegistry, SourceAdapter, ScanCoordinator, Normalizer, Deduplicator, IntentFilter, LocationResolver, LeadScorer, LocalModelClient, TemplateEngine, ConversationRouter, OwnershipService, TelegramBridge, OutboxDispatcher, ReplyTracker, Scheduler, ReportGenerator, SecretStore, BackupService ve HealthMonitor.
Her modülün sorumluluğunu, giriş/çıkışını, hata tipini ve yan etkisini açıkla. Repo klasör ağacı, paket sınırları ve bağımlılık yönü ver. Saf kuralları ağ ve UI'dan ayır.

KAYNAK ADAPTÖRÜ SÖZLEŞMESİ
- capabilities(), test_connection(), discover_updates(cursor), fetch_thread(conversation_id), send_reply(target, body, idempotency_key), reconcile_send(attempt), isteğe bağlı attachments ve direct_messages.
- Bir adaptörün yalnızca discover/read sunması geçerlidir; yazma yeteneği yoksa send çağrısı yapılamaz.
- cursor, pagination, ETag, 429/Retry-After, zaman aşımı, artan bekleme, kaynak başına hız sınırı, devre kesici ve iptal modeli.
- Erişim engeli/CAPTCHA/giriş süresi bitişi ayrı hata; engel aşma sistemi tasarlama.
- Kaynaklar: Technopat, Techolay, DonanımHaber, Donanım Arşivi, ShiftDelete.Net ve R10 araştırma adaylarıdır; mevcut RSS/API/yazma yetkisini varsayma. Google Alerts isteğe bağlı keşif girdisi. Discord/Telegram yalnızca erişim verilen kanallarda. Sosyal platformlar için genel tarama varsayımı yok.
- En az bir gerçek okuma adaptörü bağlantı testinden geçsin. Köprü pilotu için kullanıcının kontrolündeki bir test kanalı/grubu kullanılabilir; bunu kamu forumunda çalışan otomasyon diye sunma.

VERİ MODELİ
Şu tabloları alanları, foreign key'leri, nullable anlamları, indeksleri ve unique kısıtlarıyla tasarla: service_profiles, service_areas, sources, source_capabilities, scan_runs, source_cursors, raw_posts, post_revisions, leads, score_evidence, conversations, participants, templates, model_runs, draft_messages, approvals, outbox_messages, send_attempts, inbound_messages, delivery_receipts, telegram_mappings, telegram_updates, attachment_records, conversation_ownership, event_log, daily_reports, settings, schema_migrations.
- Kaynak+external_message_id benzersiz; konu ID ve mesaj ID ayrı.
- Telegram chat_id + message_id eşleştirmesi; forum konusu kullanılıyorsa message_thread_id ekle. Telegram kimlikleri için 64 bit güvenli saklama.
- Kaynak mesajından Telegram mesajına ve Telegram mesajından kaynak mesajına yönlü eşleştirme.
- Özel mesaj, genel konu ve aynı kişinin farklı konuşmaları birbirine karıştırılmaz.
- Zamanlar UTC, kullanıcı görünümü ve günlük rapor Europe/Istanbul.
- SQLite WAL, kısa transaction, yazma seri hale getirme ve busy timeout; kuyruk kalıcılığı. Şema migration ve yedek geri alma planı.
- Ham içerik saklama süresi, müşteri notları ve mesaj eşleştirmelerinin saklama politikalarını ayrı tanımla. Gizli bilgiler sıradan DB alanında düz metin tutulmaz.

MESAJ GÜVENİLİRLİĞİ VE SAHİPLİK
1. İçeriği kalıcılaştırmadan tarama cursor'u ilerletme.
2. Telegram update_id işlemesini, durable inbox kaydını ve cursor ilerlemesini veri kaybı yaratmayacak biçimde tasarla. Geçmiş güncellemelerin sonsuza kadar tutulacağını varsayma; Telegram saklama sınırını resmî belgelerden doğrula ve uzun çevrimdışı boşlukları raporla.
3. Outbox durumları: draft, awaiting_approval, queued, sending, confirmed, failed, uncertain, cancelled. HTTP 200 her adaptörde mesajın yazıldığı anlamına gelmez.
4. “Tam bir kez” dış teslimat garantisi iddia etme. Kalıcı idempotency, message ID ve uzlaştırmayla çift gönderim riskini azalt. Belirsiz sonuçta otomatik tekrar yapma.
5. Devralma transaction içinde sahiplik sürümünü artırır, bekleyen otomatik gönderimleri iptal eder. Dispatcher gerçek gönderimden hemen önce sürüm/sahiplik/izin/tazelik kontrolü yapar. Zaten dış servise çıkmış isteğin geri alınamayabileceğini açıkça ele al.
6. Aynı bilgisayarda ikinci uygulama örneği ve aynı bot tokenıyla iki poller çalışmasını engelle veya görünür hata üret.
7. Köprü döngüsünü önlemek için origin, correlation_id ve kendi gönderilerimizin harici ID'lerini kullan. Bot mesajı kaynakta tekrar görüldüğünde yeni müşteri dönüşü sayılmaz.
8. Uzun metinleri hedef limitine göre sıralı parçala; tüm parçaların kimliğini ve kısmi gönderim durumunu sakla.
9. Bilgisayar çevrimdışıyken Telegram mesajlarının hemen iletilmediği UI'da açık olsun. Eski kuyruk mesajları için TTL ve yeniden onay politikası tanımla.

TELEGRAM KÖPRÜSÜ
- Yerel bilgisayarda long polling varsayılan; açık port veya herkese açık webhook sunucusu zorunlu değil. Ağ istemci bağlantıları normal şekilde kullanılır.
- Bot kurulumu, token testi, kullanıcı kimliği doğrulama, bir defalık eşleştirme kodu ve chat/user allowlist akışı.
- Özel sohbette Reply ile yönlendirme temel seçenek. Yetki verilmiş forum özellikli grupta müşteri başına konu isteğe bağlı. Botun her grup veya konuyu oluşturabildiğini varsayma; yetenek testi yap.
- Eşleştirme yoksa gönderim durur. Serbest mesni “en son müşteriye gönder” şeklinde yönlendirme.
- Düğmeler: Gönder, Düzenle, Geç, Devral, Taslak öner, Kaynağı aç, Randevu, İş alındı, Kapat. Komutlar: /status, /pause, /resume, /stop_sending, /report, /help. /resume tarama ile gönderim kilidini ayrı yönetir.
- Callback'lerde de user/chat yetkilendirmesi, süre aşımı ve işlem tekrarı denetimi yap. Model ürettiği metinle bot komutu çalıştıramaz.
- Metin, resim, belge ve desteklenmeyen içerik davranışları; HTML/Markdown escape, dosya türü/uzunluğu, limitler ve hata mesajları.
- Token yerel secret store/Windows Credential Manager gibi uygun sistem deposunda; log, yedek ve hata raporunda gizlenir. Token değiştirme ve iptal prosedürü.

YEREL MODEL VE KURAL MOTORU
- Önce ucuz kurallar: dil/anahtar ifade, olumsuzluk, tarih, hizmet uyumu, açık konum, tekrar kontrolü. Yerel model yalnızca adaylarda; tüm geçmişi modele yükleme.
- Görevler: hizmet niyeti sınıflandırma, bilgi eksiklerini çıkarma, kısa ilk cevap ve kullanıcıya taslak önerisi. Otomatik fiyat pazarlığı ve randevu onayı yok.
- Yapılandırılmış çıktı örneği: intent, service_type, location_evidence, missing_fields, suggested_reply, needs_review. JSON şeması ve izinli değerler; kullanıcı içeriğinden eylem çalıştırma yok.
- Yanıt taslağı uygulamanın fiyat/müsaitlik/iletişim kurallarıyla deterministik doğrulanır. Geçersiz çıktı şablona düşer veya inceleme ister; sonsuz yeniden üretim yok.
- Dış mesajlar güvenilmeyen veri: prompt injection ayrımı, bağlam sınırlama, araçsız model, erişim sırlarının bağlama girmemesi.
- Model isteğe bağlı indirilsin; dosya boyutu, lisans, hash ve RAM hedefi görünür. Kullanıcı onayı olmadan büyük indirme veya GPU yükü başlatma.
- Tek inference işi, sınırlandırılmış kuyruk, iptal/zaman aşımı, azami giriş/çıkış tokenı, boşta modeli boşaltma seçeneği. Telegram manuel mesaj iletimi model kuyruğunu beklemez.
- Küçük modelin Türkçe kalitesini ölçmek için satış ilanı, belirsiz konum, negasyon ve açık hizmet ihtiyacı içeren örnek kümesi. Sahte doğruluk yüzdesi yazma.

PERFORMANS HEDEFLERİ — ÖLÇÜLECEK, GARANTİ DEĞİL
Model hariç boşta toplam uygulama RAM hedefi 350 MB altında; karşılanamazsa ölçümü ve nedeni raporla. Model için toplam süreç ağacı belleğini ayrıca raporla. Arayüzde ağ/model sırasında donma olmaması; uzun işler iptal edilebilir. İlk ayar önerisi iki HTTP kaynağı eşzamanlı, kaynak başına 10–30 dakika tarama; gerçek kaynak sınırı önceliklidir. Tarayıcı adaptörü en fazla bir etkin oturumla başlasın. Sabit ve ölçülmemiş “çok hafif” iddiası yerine CPU/RAM/yanıt süresi ölçüm yöntemi ver. Ağ ve kaynak bekleme süresini yerel işlem süresinden ayır.

DOĞRULAMA VE TESLİM
- Birim: Türkçe normalizasyon, niyet/negasyon, konum kanıtı, puanlama ve dedup.
- Entegrasyon: SQLite migration, inbox/outbox, Telegram routing, izinler, yeniden başlatma ve ownership yarışları.
- Adaptör: kayıtlı fixture ile ayrıştırma; canlı okuma denemesi ayrı. Yazma testi yalnızca belirlenmiş test konuşmasında.
- Uçtan uca: kaynak talebi → onay → ilk cevap → müşteri dönüşü → Telegram bildirimi → kullanıcının Reply cevabı → doğru kaynakta doğrulanmış gönderim.
- Hata enjeksiyonu: zaman aşımı, 429, oturum kaybı, model kapalı, Telegram kesintisi, çöken motor, DB kilidi, desteklenmeyen dosya ve belirsiz teslimat.
- Paketleme: Windows EXE/kurulum seçeneği, temiz Windows denemesi, gereken Qt/SQLite/ağ bağımlılıkları, opsiyonel model ve tarayıcı dosyaları ayrı. Sürüm/yapı numarası, migration, kaldırmada veri koruma ve güncelleme geri dönüşü. Kod imzalama maliyetini sıfır varsayma.
- Ağ arızasında uygulama eski veriyi silmez. Çalışmayan adaptör demo verisiyle başarılı görünmez. Test edilmemiş özelliği açıkça belirt.

İSTENEN TEKNİK BELGE
1. Mimari karar kayıtları ve alternatiflerin kısa gerekçesi.
2. Repo/paket yapısı ve modül sözleşmeleri.
3. Veri şeması, unique/index stratejisi, migration ve veri yaşam döngüsü.
4. Kritik akışlar ve durum makineleri; gerekirse küçük Mermaid diyagramları.
5. Telegram eşleştirme, gönderim uzlaştırma, sahiplik kilidi ve döngü önleme algoritmaları.
6. Model sözleşmesi, güvenlik ve performans ölçüm planı.
7. Kaynak başına erişim doğrulama matrisi; varsayımlar ve gerçek engeller.
8. Küçük uygulama aşamaları, her aşamanın kabul testi ve beklenen teslimi.
9. Geliştirme başlayınca kullanılacak komutlar, paketleme ve test planı; çalıştırılmamış komutları başarıyla çalıştı diye yazma.

Geliştirme sırası: önce yerel veri/arayüz ve kontrollü Telegram köprüsü; ardından gerçek kaynak okuma pilotu; sonra doğrulanmış kaynakta onaylı ilk cevap; son olarak ölçülmüş yerel model ve kaynak bazlı otomatik ilk cevap. Kaynak erişimi çözülmeden bütün sitelerde otomatik gönderim vaat etme.
```
