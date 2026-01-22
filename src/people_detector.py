from ultralytics import YOLO
import cv2
import os

def run_detector():
    model = YOLO("yolov8n.pt")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mot_dir = os.path.join(base_dir, "datasets", "mot")
    output_dir = os.path.join(base_dir, "runs", "karsilastirma")
    os.makedirs(output_dir, exist_ok=True)

    video_source = "crowd-people.mp4"
    video_path = os.path.join(mot_dir, video_source)

    if not os.path.exists(video_path):
        print(f"Video bulunamadi: {video_path}")
        return

    print(f"Islemiyor: {video_source}")
    cap = cv2.VideoCapture(video_path)

    w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    video_out_name = f"track_byte_{video_source}"
    video_output_path = os.path.join(output_dir, video_out_name)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (w_frame, h_frame))

    frame_count = 0

    unique_ids = set()

    while True:
        ret, frame = cap.read()
        if not ret: 
            break

        frame_count += 1

        tracker_config = os.path.join(base_dir, "configs", "custom_bytetrack.yaml")
        if not os.path.exists(tracker_config):
            tracker_config = "bytetrack.yaml"
                
        results = model.track(frame, verbose=False, tracker=tracker_config, conf=0.55, iou=0.5, persist=True)

        current_frame_people = 0

        for r in results:
            boxes = r.boxes
            if boxes.id is not None:
                boxes_xyxy = boxes.xyxy.cpu()
                boxes_cls = boxes.cls.cpu().tolist()
                boxes_id = boxes.id.cpu()
        
                for box, cls, id in zip(boxes_xyxy, boxes_cls, boxes_id):
                    if int(cls) != 0: 
                        continue
                    
                    current_id = int(id)
                    unique_ids.add(current_id)
                    current_frame_people += 1

                    x1, y1, x2, y2 = box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, f"ID: {current_id}", (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(frame, f"TOTAL UNIQUE: {len(unique_ids)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"CURRENT: {current_frame_people}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
        out.write(frame)
        cv2.imshow("TEST", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    unique_id_count = len(unique_ids)
    print(f"Bitti: {video_path} | Toplam Tespit Edilen Tekil İnsan: {unique_id_count}")

if __name__ == "__main__":
    run_detector()