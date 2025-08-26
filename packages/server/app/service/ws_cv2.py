import cv2
import base64
import asyncio
from socketio import AsyncServer

async def stream_webcam(sio: AsyncServer):
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            continue
        _, buffer = cv2.imencode(".jpg", frame)
        frame_b64 = base64.b64encode(buffer).decode("utf-8")
        await sio.emit("frame", {"image": frame_b64})
        await asyncio.sleep(0.05) 
