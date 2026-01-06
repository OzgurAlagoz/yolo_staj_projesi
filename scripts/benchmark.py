import os
import sys
import yaml
import time
import torch
from ultralytics import YOLO

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.utils.logger import BenchmarkLogger
except ImportError:
    print("UYARI: Logger bulunamadi, sonuclar sadece ekrana yazilacak.")
    BenchmarkLogger = None

def run_benchmark():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dataset_root = os.path.join(base_dir, "datasets", "coco")

    config_path = os.path.join(base_dir, "configs", "benchmark.yaml")
    original_data_yaml = os.path.join(base_dir, "configs", "coco.yaml")

    temp_data_yaml = os.path.join(base_dir, "configs", "coco_temp.yaml")

    print(f"Veri seti yolu ayarlaniyor: {dataset_root}")
    
    with open(original_data_yaml, 'r') as f:
        data_config = yaml.safe_load(f)

    data_config['path'] = dataset_root

    with open(temp_data_yaml, 'w') as f:
        yaml.dump(data_config, f)

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    print(f"\nBENCHMARK BASLIYOR: {config['experiment_name']}")
    print(f"==================================================")

    logger = None
    if BenchmarkLogger:
        logger = BenchmarkLogger(save_dir=os.path.join(base_dir, "runs"))

    if torch.cuda.is_available() and config['settings']['device'] == 0:
        device = 0
        device_name = torch.cuda.get_device_name(0)
    else:
        device = 'cpu'
        device_name = 'CPU'
    
    print(f"💻 Kullanılan Cihaz: {device} ({device_name})")

    for model_name in config['models']:
        print(f"\nSiradaki Model: {model_name}")
        
        try:
            model = YOLO(model_name)
        except Exception as e:
            print(f"HATA: {model_name} yüklenemedi. {e}")
            continue

        print("Predict...")
        try:
            model.predict(os.path.join(dataset_root, "images"), max_det=1, verbose=False, device=device, stream=True)
            list(model.predict(os.path.join(dataset_root, "images"), max_det=1, verbose=False, device=device, stream=True))
        except:
            pass

        print("(500 resim taraniyor)...")
        
        start_time = time.time()

        results = model.val(
            data=temp_data_yaml,
            imgsz=config['settings']['imgsz'],
            conf=config['settings']['conf'],
            iou=config['settings']['iou'],
            device=device,
            verbose=False,
            plots=False
        )
        
        end_time = time.time()
        total_time = end_time - start_time

        map50_95 = results.box.map
        map50 = results.box.map50
        
        metrics = {
            'metrics/mAP50-95(B)': map50_95,
            'metrics/mAP50(B)': map50
        }

        num_images = 500 
        fps = num_images / total_time
        latency = (total_time / num_images) * 1000

        print(f"SONUCLAR -> mAP50: {map50:.3f} | FPS: {fps:.2f}")

        if logger:
            logger.log_result(model_name, str(device_name), metrics, fps, latency)

    if os.path.exists(temp_data_yaml):
        os.remove(temp_data_yaml)
        print("\nGecici ayar dosyasi temizlendi.")

    print("\nSonuclar 'runs/results.csv' dosyasina kaydedildi.")

if __name__ == "__main__":
    run_benchmark()