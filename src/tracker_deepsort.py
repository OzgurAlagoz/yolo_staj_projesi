from ultralytics import YOLO
import os
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

tracker = DeepSort(max_age=30)
model = YOLO("yolov8n.pt")
source = "https://github.com/intel-iot-devkit/sample-videos/raw/master/people-detection.mp4"
cap = cv2.VideoCapture(source)

w_frame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h_frame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

output_video_path = "demo_output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (w_frame, h_frame))

results_file = open("results.txt", "w")
frame_count = 0

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
        ltrb = track.to_ltrb()

        x1, y1, x2, y2 = int(ltrb[0]), int(ltrb[1]), int(ltrb[2]), int(ltrb[3])

        w_current = x2 - x1
        h_current = y2 - y1

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, "ID: " + str(track_id), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        line = f"{frame_count},{track_id},{x1},{y1},{w_current},{h_current},1,-1,-1,-1\n"
        results_file.write(line)

    out.write(frame)
    cv2.imshow("DeepSORT Tracker", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

results_file.close()
cap.release()
out.release()
cv2.destroyAllWindows()

