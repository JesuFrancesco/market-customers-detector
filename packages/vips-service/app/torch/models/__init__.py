import os

ARCFACE_MODEL_PATH = os.path.join(os.path.dirname(__file__), "arcface.onnx")
YOLOV8_FACE_MODEL_PATH = os.path.join(os.path.dirname(__file__), "yolov8n-face-lindevs.pt")

__all__ = ["ARCFACE_MODEL_PATH", "YOLOV8_FACE_MODEL_PATH"]
