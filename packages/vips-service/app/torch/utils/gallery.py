import os
import cv2
import glob
import numpy as np
from typing import List, Dict
from ultralytics import YOLO
from insightface.model_zoo import ArcFaceONNX

from app.torch.embedding import embed_face
from app.torch.detection import detect_faces, align_face
from app.torch.utils.math import l2_normalize, largest_box
from app.logger import setup_logger

logger = setup_logger(__name__)

def read_images(folder: str) -> List[np.ndarray]:
    imgs = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.bmp"):
        for p in glob.glob(os.path.join(folder, ext)):
            img = cv2.imread(p)
            if img is not None:
                imgs.append(img)
    return imgs

def build_gallery(yolo: YOLO, arcface: ArcFaceONNX, gallery_dir: str) -> Dict[str, np.ndarray]:
    """
    Build mean-embedding per person from gallery folders.
    Structure:
      gallery/
        Alice/ *.jpg
        Bob/   *.jpg
    Returns dict: { name: 512-D embedding }
    """
    logger.info(f"[Gallery] Building from: {gallery_dir}")
    db: Dict[str, np.ndarray] = {}
    if not os.path.isdir(gallery_dir):
        logger.warning("[Gallery] Directory not found; starting empty.")
        return db

    people = [d for d in sorted(os.listdir(gallery_dir))
              if os.path.isdir(os.path.join(gallery_dir, d))]
    for person in people:
        person_dir = os.path.join(gallery_dir, person)
        images = read_images(person_dir)
        embs = []
        for img in images:
            faces = detect_faces(yolo, img)
            if not faces:
                continue
            best_idx = largest_box([f["xyxy"] for f in faces])
            if best_idx < 0:
                continue
            aligned = align_face(img, faces[best_idx])
            if aligned is None:
                continue
            emb = embed_face(arcface, aligned)
            embs.append(emb)
        if embs:
            mean_emb = np.mean(np.stack(embs, axis=0), axis=0)
            mean_emb = mean_emb.flatten()
            db[person] = l2_normalize(mean_emb.astype(np.float32))
            logger.info(f"[Gallery] {person}: {len(embs)} faces -> enrolled.")
        else:
            logger.warning(f"[Gallery] {person}: no valid faces found; skipped.")
            
    logger.info(f"[Gallery] Enrolled identities: {list(db.keys())}")
    return db
