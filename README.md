# YOLO Nesne Tespiti ve Takibi Projesi

Bu proje, YOLOv8, YOLOv5 ve YOLOv9 modellerinin performanslarını karşılaştırmak (benchmark) ve nesne takibi (object tracking) yeteneklerini test etmek amacıyla geliştirilmiştir.

Proje kapsamında COCO veri setinin "Person" (İnsan) alt kümesi ve MOT17 örnek videoları kullanılarak; modellerin çıkarım hızı (FPS), doğruluğu (mAP) ve donanım üzerindeki yükü analiz edilmektedir.

## Proje Yapısı

Proje dosyaları aşağıdaki düzendedir:

* configs/: Benchmark ve model parametrelerinin bulunduğu ayar dosyaları (YAML).
* datasets/: Veri setlerinin indirildiği klasör. (Git deposuna dahil edilmez, script ile oluşturulur).
    * coco/: Eğitim ve test resimleri ile YOLO formatındaki etiket dosyaları.
    * mot/: Tracking testleri için kullanılan video dosyaları.
* scripts/: Veri indirme, format dönüştürme ve benchmark testleri için kullanılan Python scriptleri.
* src/: Projenin ana kaynak kodları (Loglama araçları vb.).
* runs/: Deney sonuçlarının (CSV) ve çıktıların kaydedildiği klasör.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

1. Projeyi Klonlama:
Projeyi bilgisayarınıza indirin ve proje dizinine gidin.

2. Sanal Ortam Oluşturma:

# Windows için:
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac için:
python3 -m venv .venv
source .venv/bin/activate

3. Kütüphanelerin Yüklenmesi (ÖNEMLİ):
Standart kurulum için requirements dosyasını kullanabilirsiniz. Ancak NVIDIA ekran kartı (GPU) hızlandırmasından yararlanmak için PyTorch'un CUDA sürümünü kurmanız şiddetle önerilir.

# Adım 3.1: Önce temel gereksinimleri kurun
pip install -r requirements.txt

# Adım 3.2: Eğer NVIDIA Ekran Kartınız varsa, mevcut torch'u silip CUDA destekli olanı kurun (Performans için şarttır)
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

## Kullanım

### 1. Veri Hazırlığı
Verileri (COCO resimleri ve MOT videoları) otomatik olarak indirmek ve YOLO formatına hazırlamak için:

python scripts/prepare_data.py

### 2. Benchmark Testi (Performans Ölçümü)
YOLOv8n, YOLOv5su ve YOLOv9c modellerini sırasıyla çalıştırıp hız (FPS) ve doğruluk (mAP) değerlerini ölçmek için:

python scripts/benchmark.py

*Not: Script, bilgisayarınızdaki donanımı (CPU/GPU) otomatik algılar ve sonuçları `runs/results.csv` dosyasına kaydeder.*

## Deney Sonuçları (Gerçek Veriler)

Aşağıdaki sonuçlar **NVIDIA GeForce GTX 1660 SUPER** donanımı üzerinde, 500 adetlik COCO-Person alt kümesi kullanılarak alınmıştır.

| Model | Boyut | Hız (Inference Time) | Başarı (mAP50) | Yorum |
| :--- | :--- | :--- | :--- | :--- |
| **YOLOv8n** | Nano | **~3.2 ms** (312 FPS) | 0.135 | En hızlı model. Gerçek zamanlı uygulamalar için ideal. |
| **YOLOv5su** | Small | ~5.8 ms (172 FPS) | 0.136 | v8n ile benzer doğrulukta, ancak biraz daha yavaş. |
| **YOLOv9c** | Compact | ~53.6 ms (18 FPS) | **0.163** | En yüksek doğruluk (+%20 fark). Karmaşık sahnelerde daha yetenekli. |

*Detaylı metrikler için `runs/results.csv` dosyasına bakabilirsiniz.*

## Ayarlar

Test parametreleri 'configs/benchmark.yaml' dosyasında tanımlanmıştır. Modeller listesi, resim boyutu (imgsz), güven eşiği (conf) ve diğer parametreler buradan değiştirilebilir.

## Proje Durumu

* [x] **Gün 1:** Kurulum, repo yapısının oluşturulması ve veri hazırlığı (Tamamlandı).
* [x] **Gün 2:** CUDA/GPU entegrasyonu ve Benchmark testlerinin yapılması (Tamamlandı).
* [ ] **Gün 3:** Sonuçların grafikleştirilmesi ve detaylı analizi.
* [ ] **Gün 4:** Nesne takibi (Object Tracking) senaryolarının uygulanması.
* [ ] **Gün 5:** API geliştirme ve Canlı test.

## Notlar

* `datasets/` klasörü boyutları nedeniyle Git'e yüklenmemiştir. Scriptler ile yerel olarak oluşturulur.
* `runs/` klasöründe sadece `results.csv` dosyası versiyon kontrolüne alınmıştır; model dosyaları ve geçici çıktılar yoksayılmıştır.