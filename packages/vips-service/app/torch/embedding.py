import numpy as np
from typing import Dict, Tuple
from app.torch.utils.math import l2_normalize, cosine_sim
from app.torch.config import (
    COS_THRESH
)

def embed_face(arcface, aligned_bgr: np.ndarray) -> np.ndarray:
    """
    Get 512-D ArcFace embedding (unit-normalized).
    """
    feat = arcface.get_feat(aligned_bgr)  # sometimes returns (1,512)
    feat = np.array(feat).flatten()       # <- ensure shape (512,)
    return l2_normalize(feat.astype(np.float32))

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