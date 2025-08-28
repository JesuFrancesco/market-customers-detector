"""Módulo de configuraciones para los modelos de CNN"""

import os

GALLERY_DIR  = os.path.join(os.path.dirname(__file__), "data", "gallery")          # folder with subfolders per person
CAPTURE_DIR  = os.path.join(os.path.dirname(__file__), "data", "captures")         # where snapshots are saved with 's'
CONF_THRESH  = 0.5                # YOLO confidence threshold
IOU_NMS      = 0.5                # YOLO NMS threshold
COS_THRESH   = 0.35               # Recognition threshold (tune for your data)
MAX_WIDTH    = 1280               # Resize camera frames if wider than this
ARCFACE_CTX  = 0                  # 0 for first GPU, -1 for CPU

