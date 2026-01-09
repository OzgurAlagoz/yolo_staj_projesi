# YOLO Nesne Tespiti ve Takibi Projesi

Bu proje, YOLOv8, YOLOv5 ve YOLOv9 modellerinin performanslarını karşılaştırmak (benchmark) ve gelişmiş nesne takibi (object tracking) yeteneklerini test etmek amacıyla geliştirilmiştir.

Proje kapsamında COCO veri setinin "Person" (İnsan) alt kümesi ve MOT17 örnek videoları kullanılarak modellerin hızı ve doğruluğu analiz edilmektedir. Ayrıca **DeepSORT** ve **ByteTrack** algoritmaları entegre edilerek, "Görsel Hafıza (ReID)" ile "Hareket Bazlı (Kalman+IoU)" takip yöntemleri hız ve istikrar açısından kıyaslanmıştır.

## Proje Yapısı

Proje dosyaları aşağıdaki düzendedir:

* `configs/`: Benchmark ve model parametrelerinin bulunduğu ayar dosyaları (YAML).
* `datasets/`: Veri setlerinin indirildiği klasör. (Git deposuna dahil edilmez).
* `scripts/`: Veri indirme, format dönüştürme ve benchmark testleri için kullanılan scriptler.
* `src/`: Projenin ana kaynak kodları.
    * `tracker_deep.py`: **DeepSORT** algoritması ile takip ve MOT kaydı yapan modül.
    * `tracker_byte.py`: **ByteTrack** algoritması ile yüksek hızlı takip yapan modül.
* `runs/`: Deney sonuçlarının kaydedildiği klasör.
    * `karsilastirma/`: Tracker demolarının (MP4) ve kıyaslama raporunun (TXT) otomatik kaydedildiği yer.
* `results.txt`: Ham MOT formatındaki çıktı dosyası.
* `requirements.txt`: Proje bağımlılıkları.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

1. **Projeyi Klonlama:**
   Projeyi bilgisayarınıza indirin ve proje dizinine gidin.

2. **Sanal Ortam Oluşturma:**

   ```bash
   # Windows için:
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac için:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Kütüphanelerin Yüklenmesi:**
   Standart kütüphaneler ve GPU (CUDA) kurulumu için aşağıdaki komutları sırasıyla çalıştırın:
   
   ```bash
   # 1. Gereksinimleri yükle
   pip install -r requirements.txt

   # 2. GPU Performansı İçin (NVIDIA Kartınız Varsa)
   # Önce mevcut torch'u sil, sonra CUDA destekli versiyonu yükle:
   pip uninstall torch torchvision torchaudio -y
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

## Kullanım

### 1. Veri Hazırlığı
Verileri indirmek ve YOLO formatına hazırlamak için:
```bash
python scripts/prepare_data.py
```

### 2. Model Benchmark (YOLO Hız Testi)
Farklı YOLO modellerini kıyaslamak için:
```bash
python scripts/benchmark.py
```

### 3. Tracker Benchmark (DeepSORT vs ByteTrack)
İki farklı takip algoritmasını çalıştırmak ve sonuçları `runs/karsilastirma/` klasöründe toplamak için sırasıyla:

**Adım A: DeepSORT Çalıştır (ReID Özellikli)**
```bash
python src/tracker_deep.py
```
*Görsel özellikleri kullandığı için daha yavaştır ancak kalabalıkta kimlikleri daha iyi korur.*

**Adım B: ByteTrack Çalıştır (Hareket Özellikli)**
```bash
python src/tracker_byte.py
```
*Sadece matematiksel hesaplama yaptığı için çok hızlıdır (High FPS).*

**Sonuçlar:** İşlem bittiğinde `runs/karsilastirma/kiyaslama_sonuclari.txt` dosyasında her iki yöntemin FPS değerlerini görebilirsiniz.

## Deney Sonuçları

### 1. Model Kıyaslaması (GTX 1660 SUPER)

| Model | Hız (Inference) | Başarı (mAP50) | Yorum |
| :--- | :--- | :--- | :--- |
| **YOLOv8n** | **~3.2 ms** (312 FPS) | 0.135 | Gerçek zamanlı takip için seçildi. |
| **YOLOv5su** | ~5.8 ms (172 FPS) | 0.136 | Benzer doğruluk, daha yavaş. |
| **YOLOv9c** | ~53.6 ms (18 FPS) | **0.163** | Yüksek doğruluk, düşük hız. |

### 2. Tracker Kıyaslaması (Örnek)

| Algoritma | FPS (Tahmini) | Yöntem | Avantajı |
| :--- | :--- | :--- | :--- |
| **DeepSORT** | ~15-20 FPS | Görsel (CNN) + Kalman | Uzun süreli kayıplarda (occlusion) kimliği korur. |
| **ByteTrack** | ~40-50 FPS | IOU + Kalman | Çok hızlıdır ve düşük skorlu nesneleri de izler. |

## Ayarlar

* **ByteTrack Ayarları:** `configs/custom_bytetrack.yaml` dosyasından eşik değerleri (track_thresh, match_thresh) değiştirilebilir.
* **Genel Ayarlar:** `configs/benchmark.yaml` dosyasından model seçimi yapılabilir.

## Proje Durumu

* [x] **Gün 1:** Kurulum, repo yapısının oluşturulması ve veri hazırlığı.
* [x] **Gün 2:** CUDA/GPU entegrasyonu ve Benchmark testleri.
* [x] **Gün 3:** En uygun modelin seçimi (YOLOv8n) ve Tracking demosu.
* [x] **Gün 4:** DeepSORT entegrasyonu ve MOT formatında loglama.
* [x] **Gün 5:** ByteTrack entegrasyonu, Tracker Kıyaslama Sistemi ve Raporlama.

## Notlar

* `runs/` klasörü altındaki video dosyaları `.gitignore` ile engellenmiştir, sadece sayısal sonuçlar (txt/csv) repoya yüklenir.
* Proje, MOT Challenge standartlarına uygun çıktı üretir.