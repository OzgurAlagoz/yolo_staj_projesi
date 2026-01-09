from ultralytics import YOLO
import cv2
import time
import os

model = YOLO("yolov8n.pt")
source = "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"
cap = cv2.VideoCapture(source)

frame_count = 0

w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

project_root = "runs"
sub_folder = "karsilastirma"
output_dir = os.path.join(project_root, sub_folder)
os.makedirs(output_dir, exist_ok=True)

video_output_path = os.path.join(output_dir, "track_byte_demo.mp4")
txt_output_path = os.path.join(output_dir, "kiyaslama_sonuclari.txt")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_output_path, fourcc, fps, (w_frame, h_frame))

baslangic_zamani = time.time()
while True:
    ret, frame = cap.read()
    if not ret: break
    
    frame_count += 1
    
    results = model.track(frame, verbose=False, tracker="configs/custom_bytetrack.yaml")

    for r in results:
        boxes = r.boxes

        if boxes.id is not None:
            boxes_xyxy = boxes.xyxy.cpu()
            boxes_cls = boxes.cls.cpu().tolist()
            boxes_conf = boxes.conf.cpu()
            boxes_id = boxes.id.cpu()

            for box, cls, conf, id in zip(boxes_xyxy, boxes_cls, boxes_conf, boxes_id):
                if int(cls) != 0: continue

                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                cv2.putText(frame, "ID: " + str(int(id)), (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    out.write(frame)
    cv2.imshow("TEST",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

bitis_zamani = time.time()
cap.release()
out.release()
cv2.destroyAllWindows()

fps_degeri = frame_count / (bitis_zamani- baslangic_zamani)
print(f"FPS: {fps_degeri}")

with open(txt_output_path, "a") as f:
    f.write(f"Tracker: ByteTrack | FPS: {fps_degeri:.2f} | Tarih: {time.ctime()}\n")