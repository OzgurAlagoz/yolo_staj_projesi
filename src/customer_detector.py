from ultralytics import YOLO
import cv2
import os
import numpy as np

def run_detector():
    model = YOLO("yolov8n.pt")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mot_dir = os.path.join(base_dir, "datasets", "mot")
    output_dir = os.path.join(base_dir, "runs", "karsilastirma")
    os.makedirs(output_dir, exist_ok=True)

    video_source = "store.mp4"
    video_path = os.path.join(mot_dir, video_source)

    if not os.path.exists(video_path):
        print(f"Video bulunamadi: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    video_out_name = f"final_simple_{video_source}"
    video_output_path = os.path.join(output_dir, video_out_name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_output_path, fourcc, fps, (w_frame, h_frame))

    cashier_zone = np.array([
        [100, 220],
        [380, 220],
        [380, 420],
        [100, 420]
    ], np.int32)

    cashier_ids = set()
    customer_ids = set()

    while True:
        ret, frame = cap.read()
        if not ret: break

        results = model.track(frame, persist=True, classes=[0], conf=0.5, verbose=False)

        cv2.polylines(frame, [cashier_zone], isClosed=True, color=(0, 255, 255), thickness=2)

        curr_cashier_count = 0
        curr_customer_count = 0

        for r in results:
            boxes = r.boxes
            if boxes.id is not None:
                boxes_xyxy = boxes.xyxy.cpu().numpy()
                boxes_id = boxes.id.cpu().numpy()

                for box, track_id in zip(boxes_xyxy, boxes_id):
                    x1, y1, x2, y2 = map(int, box)
                    current_id = int(track_id)

                    center_point = (int((x1 + x2) / 2), int((y1 + y2) / 2))

                    is_inside = cv2.pointPolygonTest(cashier_zone, center_point, False) >= 0

                    if is_inside:
                        cashier_ids.add(current_id)

                        if current_id in customer_ids:
                            customer_ids.remove(current_id)

                        color = (0, 0, 255)
                        label = f"Kasiyer {current_id}"
                        curr_cashier_count += 1
                    else:
                        if current_id in cashier_ids:
                            color = (0, 0, 255)
                            label = f"Kasiyer {current_id}"
                            curr_cashier_count += 1
                        else:
                            customer_ids.add(current_id)
                            color = (0, 255, 0)
                            label = f"Musteri {current_id}"
                            curr_customer_count += 1

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                    cv2.circle(frame, center_point, 5, (255, 0, 0), -1)

        cv2.putText(frame, f"TOPLAM KASIYER: {len(cashier_ids)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"TOPLAM MUSTERI: {len(customer_ids)}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        out.write(frame)
        cv2.imshow("Magaza Analiz", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("İşlem bitti.")

if __name__ == "__main__":
    run_detector()