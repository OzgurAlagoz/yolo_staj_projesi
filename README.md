# YOLO Nesne Tespiti ve Takibi Projesi

Bu proje, YOLOv8 ve YOLOv5 modellerinin performanslarını karşılaştırmak (benchmark) ve nesne takibi (object tracking) yeteneklerini test etmek amacıyla geliştirilmiştir.

Proje kapsamında COCO veri setinin belirli bir alt kümesi ve MOT17 örnek videoları kullanılarak; modellerin çıkarım hızı (FPS), doğruluğu (mAP) ve donanım üzerindeki yükü analiz edilecektir.

## Proje Yapısı

Proje dosyaları aşağıdaki düzendedir:

* configs/: Benchmark ve model parametrelerinin bulunduğu ayar dosyaları (YAML).
* datasets/: Veri setlerinin indirildiği klasör. (Git deposuna dahil edilmez, script ile oluşturulur).
    * coco/: Eğitim ve test resimleri ile YOLO formatındaki etiket dosyaları.
    * mot/: Tracking testleri için kullanılan video dosyaları.
* scripts/: Veri indirme, format dönüştürme ve veri hazırlığı için kullanılan Python scriptleri.
* src/: Projenin ana kaynak kodları (Loglama araçları vb.).
* runs/: Deney sonuçlarının ve çıktıların kaydedildiği klasör.

## Kurulum

Projeyi çalıştırmak için aşağıdaki adımları takip edin.

1. Projeyi Klonlama:
Projeyi bilgisayarınıza indirin ve proje dizinine gidin.

2. Sanal Ortam ve Kütüphaneler:
Aşağıdaki komutları sırasıyla terminalde çalıştırarak ortamı kurun ve kütüphaneleri yükleyin.

# Windows için Kurulum Komutları:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac için Kurulum Komutları:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Veri Hazırlığı

Proje, verileri otomatik olarak indirmek ve hazırlamak için bir script içerir. Bu script şunları yapar:
1. COCO 2017 veri setinden annotasyon dosyasını indirir.
2. "Person" (İnsan) kategorisini filtreler.
3. Tekrarlanabilir sonuçlar almak için sabit bir seed (42) kullanarak rastgele 500 resim seçer ve indirir.
4. Etiketleri COCO formatından YOLO formatına dönüştürür.
5. Tracking testleri için örnek videoları indirir.

Verileri hazırlamak için şu komutu çalıştırın:

python scripts/prepare_data.py

## Ayarlar

Test parametreleri 'configs/benchmark.yaml' dosyasında tanımlanmıştır. Modeller, resim boyutu (imgsz), güven eşiği (conf) ve diğer parametreler buradan değiştirilebilir.

## Proje Durumu

* Gün 1: Kurulum, repo yapısının oluşturulması ve veri hazırlığı tamamlandı.
* Gün 2: Benchmark testleri (Planlanan).
* Gün 3: Sonuç analizi ve raporlama (Planlanan).
* Gün 4: Nesne takibi uygulamaları (Planlanan).
* Gün 5: API geliştirme (Planlanan).

## Notlar

* 'datasets/' ve 'runs/' klasörleri boyutları nedeniyle versiyon kontrol sistemine (Git) dahil edilmemiştir.
* Tüm deneyler tekrarlanabilirlik ilkesine uygun olarak tasarlanmıştır.