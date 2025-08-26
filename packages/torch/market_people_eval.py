import sys
from typing import Optional
from ultralytics import YOLO
from models import YOLO11_MODEL_PATH
import cv2

model: Optional[YOLO] = None

def handler():
    if not model:
        raise ValueError("¡Modelo no cargado!")
    
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO detection + tracking on the frame
        results = model.track(frame, persist=True, show=False, classes=[0])

        # Plot results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLO Detection + Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    args = sys.argv[1:]

    model = YOLO(YOLO11_MODEL_PATH)

    handler()
