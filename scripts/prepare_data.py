import os
import requests
import zipfile
import json
import random

random.seed(42)  # Tekrar üretilebilirlik için kilit

bu_dosyanin_yeri = os.path.dirname(os.path.abspath(__file__))
proje_ana_dizini = os.path.dirname(bu_dosyanin_yeri)

datasets_dir = os.path.join(proje_ana_dizini, "datasets", "coco")
images_dir = os.path.join(datasets_dir, "images")
labels_dir = os.path.join(datasets_dir, "labels")
annotations_dir = os.path.join(datasets_dir, "annotations")
mot_dir = os.path.join(proje_ana_dizini, "datasets", "mot")

print(f"Calisma Dizini: {proje_ana_dizini}")
for d in [images_dir, labels_dir, annotations_dir, mot_dir]:
    os.makedirs(d, exist_ok=True)

anno_url = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
zip_path = os.path.join(annotations_dir, "annotations_trainval2017.zip")

# 1. Annotation İndir
if not os.path.exists(zip_path):
    print("1/5 Annotation indiriliyor...")
    r = requests.get(anno_url)
    with open(zip_path, "wb") as f:
        f.write(r.content)

# 2. Zip Aç
if not os.path.exists(os.path.join(annotations_dir, "annotations")):
    print("2/5 Zip aciliyor...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(annotations_dir)

# 3. JSON Yükle
print("3/5 JSON okunuyor...")
json_path = os.path.join(annotations_dir, "annotations", "instances_val2017.json")
with open(json_path, 'r') as f:
    data = json.load(f)

person_id = next(item['id'] for item in data['categories'] if item['name'] == 'person')
person_img_ids = set()
for ann in data['annotations']:
    if ann['category_id'] == person_id:
        person_img_ids.add(ann['image_id'])

# 4. Resim İndirme (Akıllı Kontrol)
mevcut_dosyalar = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]

if len(mevcut_dosyalar) >= 500:
    print(f"    -> [ATLANDI] Klasorde zaten {len(mevcut_dosyalar)} resim var.")
    indirilen_ids = [int(f.split('.')[0]) for f in mevcut_dosyalar]
else:
    selected_ids = random.sample(list(person_img_ids), 500) # 
    print(f"    -> {len(selected_ids)} resim indiriliyor...")
    
    indirilen_ids = []
    count = 0
    for img_id in selected_ids:
        file_name = str(img_id).zfill(12) + ".jpg"
        save_path = os.path.join(images_dir, file_name)
        
        if not os.path.exists(save_path):
            try:
                r = requests.get(f"http://images.cocodataset.org/val2017/{file_name}", timeout=10)
                if r.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(r.content)
                    indirilen_ids.append(img_id)
                    count += 1
                    if count % 50 == 0: print(f"       {count}...")
            except:
                pass
        else:
            indirilen_ids.append(img_id)

print("4/5 Etiketler kontrol ediliyor.")
image_sizes = {img['id']: (img['width'], img['height']) for img in data['images'] if img['id'] in indirilen_ids}

# Var olan txt sayısına bak, eksikse yeniden oluştur
mevcut_txt = len([f for f in os.listdir(labels_dir) if f.endswith('.txt')])
if mevcut_txt < len(indirilen_ids):
    print("    -> Etiketler olusturuluyor.")
    for ann in data['annotations']:
        if ann['category_id'] == person_id and ann['image_id'] in indirilen_ids:
            img_id = ann['image_id']
            if img_id not in image_sizes: continue # Hata önleyici

            W, H = image_sizes[img_id]
            x_min, y_min, w, h = ann['bbox']
            
            x_center = (x_min + w / 2) / W
            y_center = (y_min + h / 2) / H
            w_norm = w / W
            h_norm = h / H
            
            if w_norm > 1 or h_norm > 1: continue

            txt_path = os.path.join(labels_dir, str(img_id).zfill(12) + ".txt")
            with open(txt_path, "a") as f:
                f.write(f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")
else:
    print("    -> [ATLANDI] Etiketler zaten hazir.")

# ==========================================
# BÖLÜM 4: MOT VİDEOLARI 
# ==========================================
print("5/5 Videolar kontrol ediliyor")
mot_videos = {
    "mot17_02_mini.mp4": "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4",
    "street_crowd.mp4": "https://github.com/ultralytics/assets/releases/download/v0.0.0/benchmarks.mp4",
    "highway_cctv.mp4": "https://github.com/razorhash/sample-videos/raw/master/highway.mp4"
}

for filename, url in mot_videos.items():
    save_path = os.path.join(mot_dir, filename)
    if not os.path.exists(save_path):
        print(f"    -> Indiriliyor: {filename}")
        try:
            r = requests.get(url, stream=True)
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
        except Exception as e:
            print(f"Hata: {e}")

print("\n[BASARILI]")