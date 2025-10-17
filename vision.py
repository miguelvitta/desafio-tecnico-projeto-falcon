from ultralytics import YOLO
import cv2
from db import log_event

# --- Model Initialization ---
# Loads the pre-trained YOLOv8 model for object detection.
model = YOLO('yolov8n.pt')

# --- Frame Processing Function ---
# Processes a single video frame to detect QR codes and people.
def process_frame(frame, pause=False):
    qr_detector = cv2.QRCodeDetector()
    persons_count = 0
    details = {}

    # Scans the frame for specific QR codes to toggle the pause state.
    data, _, _ = qr_detector.detectAndDecode(frame)
    if data and data.strip() == "STOP_FALCON" and not pause:
        pause = True
        log_event("pause", {"reason": "QR detected"})
        print("Pause detected by QR Code")
    elif data and data.strip() == "START_FALCON" and pause:
        pause = False
        log_event("resume", {"reason": "QR detected"})
        print("Resumed by QR Code")
    
    # If not paused, performs person detection using the YOLO model.
    if not pause:
        results = model.track(frame, classes=0, conf=0.5)
        if results and len(results[0].boxes) > 0:
            persons_count = len(results[0].boxes)
            details = {"persons_count": persons_count}
            
            # Extracts the dominant color from the first detected person's bounding box.
            bbox = results[0].boxes[0].xyxy.cpu().numpy()[0]
            x1, y1, x2, y2 = map(int, bbox)
            roi = frame[y1:y2, x1:x2]
            mean_color = cv2.mean(roi)[:3]
            details["dominant_color"] = f"RGB({int(mean_color[2])}, {int(mean_color[1])}, {int(mean_color[0])})"
            
            print(f"Detected {persons_count} person(s).")
            annotated_frame = results[0].plot()
        else:
            annotated_frame = frame
    else: 
        annotated_frame = frame
        
    return annotated_frame, persons_count, details, pause

# --- Standalone Vision Test ---
# Runs a simple webcam loop to test the frame processing logic independently.
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

        # Processes every 3rd frame to optimize performance.
        frame_count += 1
        if frame_count % 3 == 0:
            annotated_frame, _, _, pause = process_frame(frame, pause)
            cv2.imshow('Falcon Vision AI', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count %= 3
    
    cap.release()
    cv2.destroyAllWindows()

# --- Main Execution Block ---
# Entry point for running this script directly for testing purposes.
if __name__ == "__main__":
    print("Standalone test initiated. Show the 'STOP_FALCON' QR Code to pause.")
    run_vision()