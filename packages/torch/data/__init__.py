import os

SAMPLE_VIDEOS_PATH = os.path.join(os.path.dirname(__file__), "videos")
CAPTURES_PATH = os.path.join(os.path.dirname(__file__), "captures")
GALLERY_PATH = os.path.join(os.path.dirname(__file__), "gallery")

__all__ = [
    "SAMPLE_VIDEOS_PATH",
    "CAPTURES_PATH",
    "GALLERY_PATH"
]
