from ultralytics import YOLO
import cv2
from db import log_event

model = YOLO('yolov8n.pt')

def process_frame(frame, pause=False):
    qr_detector = cv2.QRCodeDetector()
    persons_count = 0
    details = {}

    data, _, _ = qr_detector.detectAndDecode(frame)
    if data and data.strip() == "STOP_FALCON" and not pause:
        pause = True
        log_event("pause", {"reason": "QR detected"})
        print("Pause detected by QR Code")
    elif data and data.strip() == "START_FALCON" and pause:
        pause = False
        log_event("resume", {"reason": "QR detected"})
        print("Resumed by QR Code")
    
    if not pause:
        results = model.track(frame, classes=0, conf=0.5)
        if results:
            persons_count = len(results[0].boxes)
            if persons_count > 0:
                details = {"persons_count": persons_count}
                if len(results[0].boxes) > 0:
                    bbox = results[0].boxes[0].xyxy.cpu().numpy()[0]
                    x1, y1, x2, y2 = map(int, bbox)
                    roi = frame[y1:y2, x1:x2]
                    mean_color = cv2.mean(roi)[:3]
                    details["dominant_color"] = f"RGB({int(mean_color[2])}, {int(mean_color[1])}, {int(mean_color[0])})"
                log_event("detection", details)
                print(f"Detected {persons_count} person(s).")
                annotated_frame = results[0].plot() if results else frame
            else:
                annotated_frame = frame
        else:
            annotated_frame = frame
    else: 
        annotated_frame = frame
    return annotated_frame, persons_count, details, pause

def run_vision():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error when opening the webcam.")
        return

    pause = False
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failure in capturing frame.")
            break

        frame_count += 1
        if frame_count % 3 == 0:
            annotated_frame, _, _ = process_frame(frame, pause)
            cv2.imshow('Falcon Vision AI', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count %= 3
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Standalone test initiated. Show the 'STOP_FALCON' QR Code to pause.")
    run_vision()
