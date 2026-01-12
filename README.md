# YOLO Nesne Tespiti ve Takibi Projesi

Bu proje, YOLOv8 modelini temel alarak gelişmiş nesne takibi (object tracking) yeteneklerini test etmek ve kıyaslamak amacıyla geliştirilmiştir.

Proje kapsamında COCO veri setinin "Person" (İnsan) alt kümesi ve **MOT17** ile diğer örnek videolar kullanılarak **DeepSORT** ve **ByteTrack** algoritmaları entegre edilmiştir. Bu sayede "Görsel Hafıza (ReID)" ile "Hareket Bazlı (Kalman+IoU)" takip yöntemleri, farklı zorluk seviyelerindeki 4 farklı video senaryosunda (okul, mağaza, kalabalık cadde vb.) hız ve istikrar açısından karşılaştırılmaktadır.

## Proje Yapısı

Proje dosyaları aşağıdaki düzendedir:

* `configs/`: Benchmark ve model parametrelerinin bulunduğu ayar dosyaları (YAML).
* `datasets/`: Veri setlerinin bulunduğu klasör. `mot/` klasörü test videolarını içerir.
* `scripts/`:
    * `prepare_data.py`: Veri indirme/hazırlama scripti.
    * `benchmark.py`: YOLO modellerinin hız karşılaştırması.
* `src/`: Tracker uygulama kodları.
    * `tracker_deepsort.py`: **DeepSORT** ile 4 MOT videosunu sırayla işleyen ve sonuçları kaydeden script.
    * `tracker_bytetrack.py`: **ByteTrack** ile 4 MOT videosunu sırayla işleyen ve sonuçları kaydeden script.
* `runs/`: Deney sonuçlarının kaydedildiği klasör.
    * `karsilastirma/`:
        * `track_byte_*.mp4`: ByteTrack ile oluşturulan takip videoları.
        * `track_deep_*.mp4`: DeepSORT ile oluşturulan takip videoları.
        * `kiyaslama_sonuclari.txt`: Her iki tracker'ın FPS değerlerini içeren log dosyası.
* `requirements.txt`: Proje bağımlılıkları.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

1. **Sanal Ortam Oluşturma:**

   ```bash
   # Windows için:
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Kütüphanelerin Yüklenmesi:**
   
   ```bash
   # 1. Gereksinimleri yükle
   pip install -r requirements.txt

   # 2. GPU Performansı İçin (NVIDIA Kartınız Varsa)
   # Önce mevcut torch'u sil, sonra CUDA destekli versiyonu yükle:
   pip uninstall torch torchvision torchaudio -y
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

## Kullanım

### 1. Veri Hazırlığı ve Model Benchmark
Verileri hazırlamak veya YOLO modellerini (v5/v8/v9) hız açısından kıyaslamak için scripts klasöründeki dosyaları kullanabilirsiniz:
```bash
python scripts/prepare_data.py
python scripts/benchmark.py
```

### 2. Tracker Kıyaslama (Otomatik Test)
Proje, `datasets/mot` klasöründeki 4 videoyu otomatik olarak işleyen iki ana script içerir. Bu scriptler çalıştırıldığında videoları okur, takibi gerçekleştirir, işlenmiş videoları kaydeder ve FPS sonuçlarını raporlar.

**Adım A: DeepSORT Çalıştır**
```bash
python src/tracker_deepsort.py
```
*Görsel özellikleri (CNN) kullandığı için "Görülmeyen Nesneler (Occlusion)" ve "Kamera Hareketi" durumlarında kimliği daha iyi korur.*

**Adım B: ByteTrack Çalıştır**
```bash
python src/tracker_bytetrack.py
```
*Görsel özellik kullanmaz, sadece hareket (Kalman Filter + IoU) analizi yapar. Çok hızlıdır ve "Düşük Güven Skorlu" nesneleri de izleyerek kesintileri önler.*

**Sonuçlar:**
İşlem bittiğinde `runs/karsilastirma/` klasörüne gidin:
* **Videolar:** `track_byte_*.mp4` ve `track_deep_*.mp4` dosyalarını izleyerek görsel kaliteyi karşılaştırın.
* **Rapor:** `kiyaslama_sonuclari.txt` dosyasını açarak hangi videoda hangi tracker'ın kaç FPS hızına ulaştığını inceleyin.

## Proje Durumu

* [x] **Gün 1:** Kurulum, repo yapısının oluşturulması ve veri hazırlığı.
* [x] **Gün 2:** CUDA/GPU entegrasyonu ve Benchmark testleri.
* [x] **Gün 3:** En uygun modelin seçimi (YOLOv8n) ve Tracking demosu.
* [x] **Gün 4:** DeepSORT entegrasyonu ve MOT formatında loglama.
* [x] **Gün 5:** ByteTrack entegrasyonu, Failure Case analizleri.
* [x] **Gün 6:** Çoklu video test otomasyonu ve sonuçların raporlanması.
* [x] **Gün 7:** Failure Case analizi ve Tuning (iyileştirme) çalışmaları.

## Raporlar

* **[Kıyaslama Sonuçları (TXT)](runs/karsilastirma/kiyaslama_sonuclari.txt):** Tüm videoların FPS ve ID sayısı metrikleri.
* **[Failure Analysis & Tuning Raporu (MD)](reports/failure_analysis_report.md):** Karşılaşılan hatalar (Occlusion, ID Switching) ve çözüm yöntemlerinin detaylı analizi.

## Notlar

* `runs/` klasörü altındaki video dosyaları `.gitignore` ile engellenmiştir, sadece sayısal sonuçlar repoya yüklenir.