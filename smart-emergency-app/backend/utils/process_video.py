import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

def process_video(video_path):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    vehicle_model = YOLO('vehicle.pt')
    plate_model = YOLO('plate.pt')

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_duration = 1 / fps if fps > 0 else 1 / 30

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('static/output.mp4', fourcc, fps, (width, height))

    roi_points = np.array([
        [int(width * 0.35), int(height * 0.45)],
        [int(width * 0.47), int(height * 0.45)],
        [width, height],
        [0, height]
    ])

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        roi_color = (0, 255, 0)

        vehicle_results = vehicle_model(frame)[0]
        plate_results = plate_model(frame)[0]

        vehicle_boxes = vehicle_results.boxes.xyxy.cpu().numpy() if vehicle_results.boxes else []
        plate_boxes = plate_results.boxes.xyxy.cpu().numpy() if plate_results.boxes else []

        for vbox in vehicle_boxes:
            vx1, vy1, vx2, vy2 = map(int, vbox)
            vehicle_rect = (vx1, vy1, vx2, vy2)

            matched_plate = None
            for pbox in plate_boxes:
                px1, py1, px2, py2 = map(int, pbox)
                plate_rect = (px1, py1, px2, py2)

                if (vehicle_rect[0] <= plate_rect[0] and vehicle_rect[1] <= plate_rect[1] and
                    vehicle_rect[2] >= plate_rect[2] and vehicle_rect[3] >= plate_rect[3]):
                    matched_plate = plate_rect
                    break

            if matched_plate:
                bottom_center = (int((vx1 + vx2) / 2), vy2)

                if cv2.pointPolygonTest(roi_points.astype(np.int32), bottom_center, False) >= 0:
                    roi_color = (0, 0, 255)

                cv2.rectangle(frame, (vx1, vy1), (vx2, vy2), (255, 255, 0), 2)
                cv2.circle(frame, bottom_center, 5, (0, 0, 255), -1)

        overlay = frame.copy()
        cv2.fillPoly(overlay, [roi_points], roi_color)
        frame = cv2.addWeighted(overlay, 0.25, frame, 0.75, 0)
        cv2.polylines(frame, [roi_points], isClosed=True, color=roi_color, thickness=2)

        out.write(frame)

        elapsed = time.time() - start_time
        if frame_duration - elapsed > 0:
            time.sleep(frame_duration - elapsed)

    cap.release()
    out.release()

