from ultralytics import YOLO
import os
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
import time

def run_tracker():
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
    
    model = YOLO("yolov8n.pt")
    
    for video_name in video_files:
        video_path = os.path.join(mot_dir, video_name)
        if not os.path.exists(video_path):
            print(f"Video bulunamadi: {video_path}")
            continue

        print(f"Islemiyor: {video_name}")
        
        tracker = DeepSort(max_age=30)
        
        cap = cv2.VideoCapture(video_path)
        
        w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        video_out_name = f"track_deep_{video_name}"
        video_output_path = os.path.join(output_dir, video_out_name)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_output_path, fourcc, fps, (w_frame, h_frame))
        
        frame_count = 0
        baslangic_zamani = time.time()
        
        # Re-initialize for unique ID counting
        unique_ids = set()

        while True:
            ret, frame = cap.read()
            if not ret: break
        
            frame_count += 1
        
            detections = []
            results = model(frame, verbose=False)
            for r in results:
                boxes = r.boxes
        
                boxes_xywh = boxes.xywh.cpu()
                classes = boxes.cls.cpu().tolist()
                confs = boxes.conf.cpu().tolist()
        
                for box, cls, conf in zip(boxes_xywh, classes, confs):
                    if int(cls) != 0:
                        continue
        
                    x, y, w, h = box
        
                    x_left = int(x - w/2)
                    y_top = int(y - h/2)
                    w_int = int(w)
                    h_int = int(h)
                    
                    detections.append([[x_left, y_top, w_int, h_int], conf, cls])
        
        
            track_results = tracker.update_tracks(detections, frame=frame)
            for track in track_results:
                if not track.is_confirmed(): continue
                track_id = track.track_id
                unique_ids.add(track_id)
                ltrb = track.to_ltrb()
        
                x1, y1, x2, y2 = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])
        
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "ID: " + str(track_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
            out.write(frame)
            cv2.imshow("DeepSORT Tracker", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        bitis_zamani = time.time()
        cap.release()
        out.release()
        
        fps_degeri = frame_count / (bitis_zamani - baslangic_zamani) if (bitis_zamani - baslangic_zamani) > 0 else 0
        unique_id_count = len(unique_ids)
        print(f"Bitti: {video_name} | FPS: {fps_degeri:.2f} | Unique IDs: {unique_id_count}")
        
        with open(txt_output_path, "a") as f:
            f.write(f"Tracker: DeepSORT | Video: {video_name} | FPS: {fps_degeri:.2f} | IDs: {unique_id_count} | Tarih: {time.ctime()}\n")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_tracker()