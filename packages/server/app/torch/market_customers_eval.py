import os
import argparse
import cv2
from ultralytics import YOLO
from app.torch.models import YOLO11_MODEL_PATH
from app.torch.data import SAMPLE_VIDEOS_PATH

print("Loading YOLO model")
model = YOLO(YOLO11_MODEL_PATH)
if not model: raise ValueError("¡Modelo no pudo cargar!")

async def cv2_track_with_yolo(cv2_window: bool = False):
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
        if cv2_window:
            cv2.imshow("YOLO Detection + Tracking", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            yield annotated_frame

    cap.release()
    cv2.destroyAllWindows()

async def mp4_track_with_yolo(cv2_window: bool = False):
    for video in os.listdir(SAMPLE_VIDEOS_PATH):
        if video.endswith(".mp4"):
            video_path = os.path.join(SAMPLE_VIDEOS_PATH, video)
            cap = cv2.VideoCapture(video_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Run YOLO detection + tracking on the frame
                results = model.track(frame, persist=True, show=False, classes=[0])

                # Plot results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                if cv2_window:
                    cv2.imshow("YOLO Detection + Tracking", annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    yield annotated_frame

            cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='YoloTrackCMarketCustomersDemo',
                    description='sample text',
                    epilog='sample text')

    parser.add_argument('--cv2', help="Usa la WebCam", action='store_true')  # on/off flag
    parser.add_argument('--mp4', help="Usar directorio de videos", action='store_true')  # on/off flag
    args = parser.parse_args()

    try:
        if args.cv2:
            cv2_track_with_yolo(cv2_window=True)

        elif args.mp4:
            mp4_track_with_yolo(cv2_window=True)
    except KeyboardInterrupt:
        print("¡Interrumpido por el usuario!")
