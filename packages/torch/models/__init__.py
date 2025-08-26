import os
model_dir = os.path.dirname(__file__)

YOLO11_MODEL_PATH = os.path.join(model_dir, "yolo11n.pt")
YOLOV8_FACE_MODEL_PATH = os.path.join(model_dir, "yolov8n-face-lindevs.pt")

__all__ = ["YOLO11_MODEL_PATH", "YOLOV8_FACE_MODEL_PATH"]
