import os

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)