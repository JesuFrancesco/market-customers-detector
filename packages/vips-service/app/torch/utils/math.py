from typing import List
from numpy.linalg import norm
import numpy as np

def l2_normalize(v: np.ndarray) -> np.ndarray:
    return v / (norm(v) + 1e-9)

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    a = np.array(a).flatten()
    b = np.array(b).flatten()
    return float(np.dot(a, b) / (norm(a) * norm(b) + 1e-9))

def largest_box(boxes: List[np.ndarray]) -> int:
    if not boxes:
        return -1
    areas = [max(0, (b[2]-b[0])) * max(0, (b[3]-b[1])) for b in boxes]
    return int(np.argmax(areas))
