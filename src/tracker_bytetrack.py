from ultralytics import YOLO
import cv2
import time
import os

def run_tracker():
    model = YOLO("yolov8n.pt")
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mot_dir = os.path.join(base_dir, "datasets", "mot")
    output_dir = os.path.join(base_dir, "runs", "karsilastirma")
    os.makedirs(output_dir, exist_ok=True)
    
    txt_output_path = os.path.join(output_dir, "kiyaslama_sonuclari.txt")
    
    video_files = [
        "classroom.mp4",
        "face-demographics-walking-and-pause.mp4",
        "mot17_02_mini.mp4",
        "store-aisle-detection.mp4"
    ]
    
    for video_name in video_files:
        video_path = os.path.join(mot_dir, video_name)
        if not os.path.exists(video_path):
            print(f"Video bulunamadi: {video_path}")
            continue
            
        print(f"Islemiyor: {video_name}")
        cap = cv2.VideoCapture(video_path)
        
        w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        video_out_name = f"track_byte_{video_name}"
        video_output_path = os.path.join(output_dir, video_out_name)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_output_path, fourcc, fps, (w_frame, h_frame))
        
        frame_count = 0
        baslangic_zamani = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret: break
            
            frame_count += 1
            
            tracker_config = os.path.join(base_dir, "configs", "custom_bytetrack.yaml")
            if not os.path.exists(tracker_config):
                tracker_config = "bytetrack.yaml"
                
            results = model.track(frame, verbose=False, tracker=tracker_config, persist=True)
            
            # ID Tracking Set
            if frame_count == 1: unique_ids = set()

            for r in results:
                boxes = r.boxes
                if boxes.id is not None:
                    boxes_xyxy = boxes.xyxy.cpu()
                    boxes_cls = boxes.cls.cpu().tolist()
                    boxes_conf = boxes.conf.cpu()
                    boxes_id = boxes.id.cpu()
        
                    for box, cls, conf, id in zip(boxes_xyxy, boxes_cls, boxes_conf, boxes_id):
                        if int(cls) != 0: continue
                        
                        unique_ids.add(int(id))

        
                        x1, y1, x2, y2 = box
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                        cv2.putText(frame, "ID: " + str(int(id)), (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
            out.write(frame)
            cv2.imshow("TEST", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        bitis_zamani = time.time()
        cap.release()
        out.release()
        
        fps_degeri = frame_count / (bitis_zamani - baslangic_zamani) if (bitis_zamani - baslangic_zamani) > 0 else 0
        unique_id_count = len(unique_ids)
        print(f"Bitti: {video_name} | FPS: {fps_degeri:.2f} | Unique IDs: {unique_id_count}")
        
        with open(txt_output_path, "a") as f:
            f.write(f"Tracker: ByteTrack | Video: {video_name} | FPS: {fps_degeri:.2f} | IDs: {unique_id_count} | Tarih: {time.ctime()}\n")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_tracker()