import sys
from ultralytics import YOLO
from models import YOLO11_MODEL_PATH, YOLOV8_FACE_MODEL_PATH
import cv2

model = None
def handler():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO detection + tracking on the frame
        results = model.track(frame, persist=True, show=False)

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

    if "--face" in args:
        print("Using face model")
        model = YOLO(YOLOV8_FACE_MODEL_PATH)
    else:
        print("Using COCO model")
        model = YOLO(YOLO11_MODEL_PATH)

    handler()
