import argparse
import asyncio
import os
import cv2
import time

# ---- YOLO (Ultralytics) ----
from ultralytics import YOLO

# ---- ArcFace (InsightFace) ----
from insightface.model_zoo import get_model

# -- Utils --
from app.logger import setup_logger
from app.torch.models import ARCFACE_MODEL_PATH, YOLOV8_FACE_MODEL_PATH
from app.torch.utils.file import ensure_dir
from app.torch.utils.math import largest_box
from app.torch.utils.gallery import build_gallery
from app.torch.detection import detect_faces, align_face
from app.torch.embedding import embed_face, match_embedding
from app.torch.utils.drawing import draw_box_label
from app.torch.config import (
    ARCFACE_CTX,
    CAPTURE_DIR,
    GALLERY_DIR,
    MAX_WIDTH,
)

# =========================
# Logger
# =========================
logger = setup_logger(__name__)

# =========================
# Models
# =========================
logger.info("Loading YOLO face detector...")
yolo = YOLO(YOLOV8_FACE_MODEL_PATH)

logger.info("Loading ArcFace embedding model...")
arcface = get_model(ARCFACE_MODEL_PATH)
arcface.prepare(ctx_id=ARCFACE_CTX)

# Ensure capture and gallery directories
ensure_dir(CAPTURE_DIR)
ensure_dir(GALLERY_DIR)

# == Async
async def async_webcam_face_recognition():
    logger.info("Not implemented")
    pass

# == Not Async
def webcam_face_recognition():
    gallery = build_gallery(yolo, arcface, GALLERY_DIR)

    cap = cv2.VideoCapture(0)  # change index if needed
    if not cap.isOpened():
        logger.error("Could not open camera.")
        return

    logger.info("Press 'q' to quit, 'r' to reload gallery, 's' to save largest face snapshot.")

    fps_ema = None
    t_prev = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            logger.warning("[Warn] Frame grab failed.")
            break

        # Resize for speed if needed
        h, w = frame.shape[:2]
        if w > MAX_WIDTH:
            scale = MAX_WIDTH / float(w)
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

        
        # Detect faces
        faces = detect_faces(yolo, frame)

        # Recognize each face
        for f in faces:
            aligned = align_face(frame, f)
            if aligned is None:
                continue
            q = embed_face(arcface, aligned)
            name, score = match_embedding(q, gallery)
            draw_box_label(frame, f["xyxy"], name, score)

        # FPS
        t_now = time.time()
        fps = 1.0 / max(1e-6, (t_now - t_prev))
        t_prev = t_now
        fps_ema = fps if fps_ema is None else (0.9 * fps_ema + 0.1 * fps)

        cv2.putText(frame, f"FPS: {fps_ema:.1f}", (12, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Recognition (YOLO + ArcFace)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        
        elif key == ord('r'):
            logger.info("[Action] Reloading gallery…")
            gallery = build_gallery(yolo, arcface, GALLERY_DIR)

        elif key == ord('s'):
            # Save largest face snapshot
            if faces:
                idx = largest_box([f["xyxy"] for f in faces])
                if idx >= 0:
                    x1, y1, x2, y2 = faces[idx]["xyxy"]
                    crop = frame[max(0, y1):y2, max(0, x1):x2]
                    if crop.size > 0:
                        ts = time.strftime("%Y%m%d_%H%M%S")
                        outp = os.path.join(CAPTURE_DIR, f"face_{ts}.jpg")
                        cv2.imwrite(outp, crop)
                        logger.info(f"[Saved] {outp}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='YoloFaceRecognitionDemo',
                    description='Pruebas en local de reconocimiento facial con YOLO y ArcFace',
                    epilog='sample text')

    parser.add_argument('--webcam', help="Usa la WebCam", action='store_true')  # on/off flag
    parser.add_argument('--mp4', help="Usar directorio de videos", action='store_true')  # on/off flag
    args = parser.parse_args()

    try:
        if args.webcam:
            logger.info("Iniciando webcam_face_recognition...")
            webcam_face_recognition()

        elif args.mp4:
            logger.warning("Not implemented !!!!")
            pass

    except KeyboardInterrupt:
        logger.info("¡Interrumpido por el usuario!")
