from ultralytics import YOLO
import os

def run_demo():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    demo_path = os.path.join(root_path, "runs", "demo")
    if not os.path.exists(demo_path):
        os.makedirs(demo_path, exist_ok=True)
    print(f"Dosya olusturuldu: {demo_path}")
    model = YOLO("yolov8n.pt")
    source = "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"
    results = model.track(source, persist=True, tracker="bytetrack.yaml",verbose=False, save=True, project=demo_path, name="demo_sonuc",stream=True)
    for i,result in enumerate(results):
        print(f"\r{i+1}.ci kare islendi.", end="")
    print(f"Video olusturuldu: {os.path.join(demo_path, 'demo_sonuc')}")
if __name__ == "__main__":
    run_demo()