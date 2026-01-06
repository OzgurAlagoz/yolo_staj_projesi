# src/utils/logger.py
import csv
import os
from datetime import datetime

class BenchmarkLogger:
    def __init__(self, save_dir="runs"):

        os.makedirs(save_dir, exist_ok=True)

        self.file_path = os.path.join(save_dir, "results.csv")
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Tarih", "Model", "Cihaz", "mAP50-95", "mAP50", "FPS", "Latency(ms)"])
            print(f"[LOG] Yeni log dosyasi olusturuldu: {self.file_path}")

    def log_result(self, model_name, device, metrics, fps, latency):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        map50_95 = round(metrics.get('metrics/mAP50-95(B)', 0), 4)
        map50 = round(metrics.get('metrics/mAP50(B)', 0), 4)

        with open(self.file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([now, model_name, device, map50_95, map50, fps, latency])
            
        print(f"[LOG] Sonuclar kaydedildi -> {model_name}")