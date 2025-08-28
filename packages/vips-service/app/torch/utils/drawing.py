import cv2
import numpy as np

def draw_box_label(frame: np.ndarray, xyxy: np.ndarray, label: str, score: float):
    """Dibuja un box label superpuesto al frame de CV2"""
    x1, y1, x2, y2 = map(int, xyxy)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 170, 255), 2)
    text = f"{label} ({score:.2f})" if score >= 0 else label
    (tw, th), bl = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    th_box = th + 10
    cv2.rectangle(frame, (x1, max(0, y1 - th_box)), (x1 + tw + 8, y1), (0, 170, 255), -1)
    cv2.putText(frame, text, (x1 + 4, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)