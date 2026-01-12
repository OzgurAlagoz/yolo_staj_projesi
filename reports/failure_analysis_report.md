# Failure Case ve Tuning Analizi Raporu

**Tarih:** 12 Ocak 2026
**Konu:** MOT (Multiple Object Tracking) Senaryolarında Hata Analizi ve İyileştirme Çalışması

## 1. Giriş
Bu çalışmada, YOLOv8 ve ByteTrack/DeepSORT algoritmalarının farklı zorluk seviyelerindeki video senaryolarında (Occlusion, Kalabalık, Hızlı Hareket) karşılaştığı başarısızlık durumları (Failure Cases) analiz edilmiş ve parametre optimizasyonu (Tuning) ile iyileştirme sağlanmıştır.

## 2. Metrikler ve Baseline Sonuçları

Aşağıdaki tablo, varsayılan ayarlarla yapılan testlerin sonuçlarını göstermektedir:

| Video Senaryosu | Tracker | FPS (Hız) | Unique ID (Tespit Edilen Kişi Sayısı) | Analiz |
| :--- | :--- | :--- | :--- | :--- |
| **Store Aisle** (Mağaza Reonu) | ByteTrack | ~39 FPS | **118** (HATA) | Videoda az kişi olmasına rağmen çok yüksek ID sayısı. Ciddi "ID Switching" var. |
| **Store Aisle** (Mağaza Reonu) | DeepSORT | ~10 FPS | **45** | Daha stabil ama çok yavaş. Yine de ID kopmaları mevcut. |
| **Classroom** (Sınıf İçi) | ByteTrack | ~25 FPS | 46 | Sınıf mevcuduna yakın makul bir sayı. |
| **Classroom** (Sınıf İçi) | DeepSORT | ~10 FPS | 12 | Occlusion nedeniyle birçok öğrenciyi kaçırmış veya tek ID altında birleştirmiş olabilir. |

## 3. Failure Case Analizi

Yapılan testlerde 3 ana başarısızlık senaryosu tespit edilmiştir:

### Case 1: ID Switching (Kimlik Karışıklığı) - *Store Aisle*
*   **Sorun:** Mağaza kamerasında kişi bir rafın arkasından geçip veya hızlıca dönüp hareket ettiğinde, tracker (özellikle ByteTrack) kişinin eski izini (track) kaybedip ona **yeni bir ID (örneğin ID #5 iken ID #12)** atamaktadır.
*   **Kanıt:** `store-aisle.mp4` videosunda gerçekte az sayıda kişi varken ByteTrack **118 farklı ID** üretmiştir. Bu, her kopmada yeni bir kişi sayıldığını gösterir.
*   **Neden:** `track_buffer` (hafıza) süresinin varsayılan değeri (30 kare) kısa kalmaktadır. Kişi 1 saniyeden fazla görünmez olduğunda unutulmaktadır.

### Case 2: Occlusion (Kapanma) - *Classroom*
*   **Sorun:** Öğrenciler birbirinin önünden geçerken arkadaki öğrenci takip edilememektedir.
*   **Kanıt:** DeepSORT sadece 12 ID bulabilmiştir. Görüntü işleme tabanlı ReID modülü, kısmi görünümlerde yeterince ayırt edici özellik çıkaramamış olabilir.

### Case 3: False Positives (Hatalı Tespit)
*   **Sorun:** Görüntüdeki cansız nesnelerin (sandalye, çanta vb.) anlık olarak insan gibi algılanıp takip başlatılması.
*   **Çözüm:** `new_track_thresh` değerini artırarak sadece çok emin olunan nesneler için takip başlatılması sağlandı.

## 4. Tuning (İyileştirme) Çalışması ve Sonuçlar

`store-aisle` senaryosundaki yüksek ID switching sorununu çözmek için `configs/custom_bytetrack.yaml` dosyasında şu değişiklikler yapılmıştır:

*   **`track_buffer`**: 30 -> **60** (İzlerin hafızada tutulma süresi 2 katına çıkarıldı).
*   **`new_track_thresh`**: 0.25 -> **0.4** (Gürültüden yeni iz oluşumu zorlaştırıldı).

**Sonuç Karşılaştırması (Store Aisle):**

| Durum | Ayarlar | FPS | Unique ID Sayısı | Yorum |
| :--- | :--- | :--- | :--- | :--- |
| **Baseline** | Varsayılan | 39.06 | **118** | Çok fazla kopma. |
| **Tuned (İyileştirilmiş)** | Buffer:60 / Thresh:0.4 | 63.38 | **85** | **%28 İyileştirme.** |

**Değerlendirme:**
Yapılan basit parametre ayarlarıyla bile ID parçalanması (fragmentation) %28 oranında azaltılmıştır. FPS değerindeki artış ise tracker'ın gereksiz gürültü izlerle uğraşmamasından kaynaklanmaktadır.

## 5. Öneriler

1.  **Kamera Açısı:** Mümkünse üstten (kuş bakışı) yerine daha karşıdan gören açılar tercih edilmelidir.
2.  **Model Eğitimi:** Kalabalık sahneler için `CrowdHuman` veriseti ile eğitilmiş modeller kullanılabilir.
3.  **Hibrid Yaklaşım:** Hız gerekmeyen yerlerde DeepSORT'un ReID özelliği, hız gereken yerlerde ByteTrack'in yüksek tampon (buffer) ayarı kullanılmalıdır.
