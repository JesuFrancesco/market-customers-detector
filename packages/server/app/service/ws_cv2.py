import cv2
import base64
import asyncio
from socketio import AsyncServer

# torch module
from app.torch.market_customers_eval import mp4_track_with_yolo, cv2_track_with_yolo

async def stream_webcam(sio: AsyncServer):
    async for annotated_frame in cv2_track_with_yolo():
        _, buffer = cv2.imencode(".jpg", annotated_frame)
        frame_b64 = base64.b64encode(buffer).decode("utf-8")
        await sio.emit("frame", {"image": frame_b64})
        await asyncio.sleep(0.05) 

async def stream_cv2(sio: AsyncServer):
    async for annotated_frame in mp4_track_with_yolo():
        _, buffer = cv2.imencode(".jpg", annotated_frame)
        frame_b64 = base64.b64encode(buffer).decode("utf-8")
        await sio.emit("frame", {"image": frame_b64})
        await asyncio.sleep(0.05) 
