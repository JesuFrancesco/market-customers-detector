import os
import argparse
import cv2
from ultralytics import YOLO
from app.torch.models import YOLO11_MODEL_PATH
from app.torch.data import SAMPLE_VIDEOS_PATH

print("Loading YOLO model")
model = YOLO(YOLO11_MODEL_PATH)
if not model: raise ValueError("¡Modelo no pudo cargar!")

# == Not Async
def webcam_track_with_yolo():
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

def mp4_track_with_yolo(video_path: str):
    if not video_path.endswith(".mp4"):
        raise ValueError("La extensión debe ser .mp4")
    
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
        cv2.imshow("YOLO Detection + Tracking", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

# == Async
async def async_webcam_track_with_yolo():
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
        yield annotated_frame

    cap.release()
    cv2.destroyAllWindows()

async def async_mp4_track_with_yolo(video_path: str):
    if not video_path.endswith(".mp4"):
        raise ValueError("La extensión ha de ser un video .mp4")
    
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
        yield annotated_frame

    cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='YoloTrackMarketCustomersDemo',
                    description='Pruebas en local de seguimiento de clientes en un mercado',
                    epilog='sample text')

    parser.add_argument('--webcam', help="Usa la WebCam", action='store_true')  # on/off flag
    parser.add_argument('--mp4', help="Usar directorio de videos", action='store_true')  # on/off flag
    args = parser.parse_args()

    try:
        if args.webcam:
            webcam_track_with_yolo()

        elif args.mp4:
            [mp4_track_with_yolo(os.path.join(SAMPLE_VIDEOS_PATH, video)) for video in os.listdir(SAMPLE_VIDEOS_PATH) if video.endswith(".mp4")]

    except KeyboardInterrupt:
        print("¡Interrumpido por el usuario!")
