import os
import cv2
import glob
import time
import numpy as np
from numpy.linalg import norm
from typing import Dict, List, Tuple

# ---- YOLO (Ultralytics) ----
from ultralytics import YOLO

# ---- ArcFace (InsightFace) ----
from insightface.model_zoo import get_model
from insightface.utils.face_align import norm_crop
from models import YOLOV8_FACE_MODEL_PATH, ARCFACE_MODEL_PATH

# =========================
# Configuration
# =========================
YOLO_WEIGHTS = YOLOV8_FACE_MODEL_PATH

GALLERY_DIR  = "gallery"          # folder with subfolders per person
CAPTURE_DIR  = "captures"         # where snapshots are saved with 's'
CONF_THRESH  = 0.5                # YOLO confidence threshold
IOU_NMS      = 0.5                # YOLO NMS threshold
COS_THRESH   = 0.35               # Recognition threshold (tune for your data)
MAX_WIDTH    = 1280               # Resize camera frames if wider than this

# If your machine has no GPU, arcface.prepare(ctx_id=-1)
ARCFACE_CTX  = 0                  # 0 for first GPU, -1 for CPU

# =========================
# Utilities
# =========================
def l2_normalize(v: np.ndarray) -> np.ndarray:
    return v / (norm(v) + 1e-9)

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    a = np.array(a).flatten()
    b = np.array(b).flatten()
    return float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def largest_face_box(boxes: List[np.ndarray]) -> int:
    """Return index of largest bbox by area."""
    if not boxes:
        return -1
    areas = [max(0, (b[2]-b[0])) * max(0, (b[3]-b[1])) for b in boxes]
    return int(np.argmax(areas))

# =========================
# Models
# =========================
print("[Init] Loading YOLO face detector...")
yolo = YOLO(YOLO_WEIGHTS)

print("[Init] Loading ArcFace embedding model...")
# Good, accurate ArcFace model (512-D) that ships with InsightFace model zoo
arcface = get_model(ARCFACE_MODEL_PATH)
arcface.prepare(ctx_id=ARCFACE_CTX)

# =========================
# Detection + Alignment
# =========================
def detect_faces(image_bgr: np.ndarray,
                 conf: float = CONF_THRESH) -> List[dict]:
    """
    Returns list of dicts: {"xyxy": np.array([x1,y1,x2,y2]), "kps": np.array([[x,y],...]) or None}
    """
    res = yolo.predict(image_bgr, conf=conf, iou=IOU_NMS, verbose=False)[0]
    out = []
    boxes_xyxy = res.boxes.xyxy.cpu().numpy().astype(int) if len(res.boxes) else []
    kps = None
    if getattr(res, "keypoints", None) is not None and res.keypoints is not None:
        # shape: (N, 5, 2) for YOLO face models (left_eye, right_eye, nose, mouth_left, mouth_right)
        kps = res.keypoints.xy.cpu().numpy()

    for i, box in enumerate(boxes_xyxy):
        item = {"xyxy": box, "kps": None}
        if kps is not None and i < kps.shape[0]:
            if kps.shape[1] >= 5:
                item["kps"] = kps[i, :5, :]
        out.append(item)
    return out

def align_face(image_bgr: np.ndarray, face: dict, image_size: int = 112) -> np.ndarray:
    """
    If 5 landmarks are available, use similarity transform alignment.
    Otherwise, center crop the bbox and resize (less accurate).
    """
    if face["kps"] is not None and face["kps"].shape[0] >= 5:
        return norm_crop(image_bgr, face["kps"], image_size=image_size)
    x1, y1, x2, y2 = face["xyxy"]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = max(x2, x1+1), max(y2, y1+1)
    crop = image_bgr[y1:y2, x1:x2]
    if crop.size == 0:
        return None
    return cv2.resize(crop, (image_size, image_size))

def embed_face(aligned_bgr: np.ndarray) -> np.ndarray:
    """
    Get 512-D ArcFace embedding (unit-normalized).
    """
    feat = arcface.get_feat(aligned_bgr)  # sometimes returns (1,512)
    feat = np.array(feat).flatten()       # <- ensure shape (512,)
    return l2_normalize(feat.astype(np.float32))

# =========================
# Gallery
# =========================
def read_images(folder: str) -> List[np.ndarray]:
    imgs = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"):
        for p in glob.glob(os.path.join(folder, ext)):
            img = cv2.imread(p)
            if img is not None:
                imgs.append(img)
    return imgs

def build_gallery(gallery_dir: str) -> Dict[str, np.ndarray]:
    """
    Build mean-embedding per person from gallery folders.
    Structure:
      gallery/
        Alice/ *.jpg
        Bob/   *.jpg
    Returns dict: { name: 512-D embedding }
    """
    print(f"[Gallery] Building from: {gallery_dir}")
    db: Dict[str, np.ndarray] = {}
    if not os.path.isdir(gallery_dir):
        print("[Gallery] Directory not found; starting empty.")
        return db

    people = [d for d in sorted(os.listdir(gallery_dir))
              if os.path.isdir(os.path.join(gallery_dir, d))]
    for person in people:
        person_dir = os.path.join(gallery_dir, person)
        images = read_images(person_dir)
        embs = []
        for img in images:
            faces = detect_faces(img)
            if not faces:
                continue
            best_idx = largest_face_box([f["xyxy"] for f in faces])
            if best_idx < 0:
                continue
            aligned = align_face(img, faces[best_idx])
            if aligned is None:
                continue
            emb = embed_face(aligned)
            embs.append(emb)
        if embs:
            mean_emb = np.mean(np.stack(embs, axis=0), axis=0)
            mean_emb = mean_emb.flatten()
            db[person] = l2_normalize(mean_emb.astype(np.float32))
            print(f"[Gallery] {person}: {len(embs)} faces -> enrolled.")
        else:
            print(f"[Gallery] {person}: no valid faces found; skipped.")
    print(f"[Gallery] Enrolled identities: {list(db.keys())}")
    return db

def match_embedding(q: np.ndarray, gallery: Dict[str, np.ndarray]) -> Tuple[str, float]:
    """
    Linear nearest neighbor search (fast enough for small galleries).
    Returns (best_name or 'Unknown', score)
    """
    best_name, best_score = "Unknown", -1.0
    for name, ref in gallery.items():
        s = cosine_sim(q, ref)
        if s > best_score:
            best_name, best_score = name, s
    if best_score < COS_THRESH:
        return "Unknown", best_score
    return best_name, best_score

# =========================
# Drawing
# =========================
def draw_box_label(frame: np.ndarray, xyxy: np.ndarray, label: str, score: float):
    x1, y1, x2, y2 = map(int, xyxy)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 170, 255), 2)
    text = f"{label} ({score:.2f})" if score >= 0 else label
    (tw, th), bl = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    th_box = th + 10
    cv2.rectangle(frame, (x1, max(0, y1 - th_box)), (x1 + tw + 8, y1), (0, 170, 255), -1)
    cv2.putText(frame, text, (x1 + 4, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)

# =========================
# Main loop
# =========================
def main():
    ensure_dir(CAPTURE_DIR)

    gallery = build_gallery(GALLERY_DIR)

    cap = cv2.VideoCapture(0)  # change index if needed
    if not cap.isOpened():
        print("[Error] Could not open camera.")
        return

    print("[Info] Press 'q' to quit, 'r' to reload gallery, 's' to save largest face snapshot.")

    fps_ema = None
    t_prev = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[Warn] Frame grab failed.")
            break

        # Resize for speed if needed
        h, w = frame.shape[:2]
        if w > MAX_WIDTH:
            scale = MAX_WIDTH / float(w)
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

        # Detect faces
        faces = detect_faces(frame)

        # Recognize each face
        for f in faces:
            aligned = align_face(frame, f)
            if aligned is None:
                continue
            q = embed_face(aligned)
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
            print("[Action] Reloading gallery…")
            gallery = build_gallery(GALLERY_DIR)
        elif key == ord('s'):
            # Save largest face snapshot
            if faces:
                idx = largest_face_box([f["xyxy"] for f in faces])
                if idx >= 0:
                    x1, y1, x2, y2 = faces[idx]["xyxy"]
                    crop = frame[max(0, y1):y2, max(0, x1):x2]
                    if crop.size > 0:
                        ts = time.strftime("%Y%m%d_%H%M%S")
                        outp = os.path.join(CAPTURE_DIR, f"face_{ts}.jpg")
                        cv2.imwrite(outp, crop)
                        print(f"[Saved] {outp}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
