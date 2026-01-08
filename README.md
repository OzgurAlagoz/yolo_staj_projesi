# YOLO Nesne Tespiti ve Takibi Projesi

Bu proje, YOLOv8, YOLOv5 ve YOLOv9 modellerinin performanslarını karşılaştırmak (benchmark) ve gelişmiş nesne takibi (object tracking) yeteneklerini test etmek amacıyla geliştirilmiştir.

Proje kapsamında COCO veri setinin "Person" (İnsan) alt kümesi ve MOT17 örnek videoları kullanılarak; modellerin çıkarım hızı (FPS), doğruluğu (mAP) ve donanım üzerindeki yükü analiz edilmektedir. Ayrıca **DeepSORT** algoritması ile görsel hafızalı takip sistemi entegre edilmiş ve çıktıların MOT formatında kaydedilmesi sağlanmıştır.

## Proje Yapısı

Proje dosyaları aşağıdaki düzendedir:

* `configs/`: Benchmark ve model parametrelerinin bulunduğu ayar dosyaları (YAML).
* `datasets/`: Veri setlerinin indirildiği klasör. (Git deposuna dahil edilmez, script ile oluşturulur).
* `scripts/`: Veri indirme, format dönüştürme ve benchmark testleri için kullanılan Python scriptleri.
* `src/`: Projenin ana kaynak kodları.
    * `tracker_deep.py`: **DeepSORT** tabanlı takip, MOT formatında kayıt ve video çıktısı üreten ana modül.
* `runs/`: Deney sonuçlarının (CSV) ve çıktıların kaydedildiği klasör.
* `results.txt`: Takip işleminin MOT formatındaki (Frame, ID, BBox...) sayısal çıktı dosyası.
* `requirements.txt`: Proje bağımlılıkları.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

1. **Projeyi Klonlama:**
   Projeyi bilgisayarınıza indirin ve proje dizinine gidin.

2. **Sanal Ortam Oluşturma:**


   # Windows için:
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac için:
   python3 -m venv .venv
   source .venv/bin/activate


3. **Kütüphanelerin Yüklenmesi (ÖNEMLİ):**
   Standart kurulum ve DeepSORT gereksinimleri için:


   pip install -r requirements.txt

   *(Not: `requirements.txt` dosyasında `ultralytics`, `deep-sort-realtime` ve `opencv-python` bulunmalıdır.)*

   **GPU Performansı İçin:** Eğer NVIDIA ekran kartınız varsa, mevcut torch'u silip CUDA sürümünü kurun:

   pip uninstall torch torchvision torchaudio -y
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

## Kullanım

### 1. Veri Hazırlığı
Verileri (COCO resimleri) otomatik olarak indirmek ve YOLO formatına hazırlamak için:

python scripts/prepare_data.py


### 2. Benchmark Testi (Performans Ölçümü)
YOLOv8n, YOLOv5su ve YOLOv9c modellerini sırasıyla çalıştırıp hız (FPS) ve doğruluk (mAP) değerlerini ölçmek için:

python scripts/benchmark.py


### 3. DeepSORT ile Takip ve MOT Kaydı
YOLOv8n modelini ve DeepSORT algoritmasını kullanarak nesne takibi yapmak, sonuçları `results.txt` dosyasına MOT formatında kaydetmek ve demo videosu oluşturmak için:


python src/tracker_deep.py

* **Çıktılar:**
    * `results.txt`: Her karenin takip verisi (MOT Challenge formatında).
    * `demo_output.mp4`: Takip işleminin görselleştirilmiş video kaydı.

## Deney Sonuçları (Gerçek Veriler)

Aşağıdaki sonuçlar **NVIDIA GeForce GTX 1660 SUPER** donanımı üzerinde, 500 adetlik COCO-Person alt kümesi kullanılarak alınmıştır.

| Model | Boyut | Hız (Inference Time) | Başarı (mAP50) | Yorum |
| :--- | :--- | :--- | :--- | :--- |
| **YOLOv8n** | Nano | **~3.2 ms** (312 FPS) | 0.135 | En hızlı model. Gerçek zamanlı tracking için seçilmiştir. |
| **YOLOv5su** | Small | ~5.8 ms (172 FPS) | 0.136 | v8n ile benzer doğrulukta, ancak biraz daha yavaş. |
| **YOLOv9c** | Compact | ~53.6 ms (18 FPS) | **0.163** | En yüksek doğruluk (+%20 fark). Hız gerekmeyen analizler için uygundur. |

*Detaylı metrikler için `runs/results.csv` dosyasına bakabilirsiniz.*

## Ayarlar

Test parametreleri `configs/benchmark.yaml` dosyasında tanımlanmıştır. Modeller listesi, resim boyutu (imgsz), güven eşiği (conf) ve diğer parametreler buradan değiştirilebilir.

## Proje Durumu

* [x] **Gün 1:** Kurulum, repo yapısının oluşturulması ve veri hazırlığı (Tamamlandı).
* [x] **Gün 2:** CUDA/GPU entegrasyonu ve Benchmark testlerinin yapılması (Tamamlandı).
* [x] **Gün 3:** En uygun modelin seçimi (YOLOv8n) ve Tracking demosu (Tamamlandı).
* [x] **Gün 4:** DeepSORT entegrasyonu, MOT formatında loglama ve Video kaydı (Tamamlandı).
* [ ] **Gün 5:** API geliştirme ve Canlı test.

## Notlar

* `datasets/` klasörü boyutları nedeniyle Git'e yüklenmemiştir. Scriptler ile yerel olarak oluşturulur.
* `results.txt` dosyası MOT değerlendirme araçlarıyla (Matlab/Python devkits) uyumludur.