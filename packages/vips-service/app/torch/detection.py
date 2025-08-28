import numpy as np
import cv2
from typing import List
from insightface.utils.face_align import norm_crop
from ultralytics import YOLO
from app.torch.config import (
    CONF_THRESH,
    IOU_NMS,
)

def detect_faces(yolo: YOLO, image_bgr: np.ndarray,
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
