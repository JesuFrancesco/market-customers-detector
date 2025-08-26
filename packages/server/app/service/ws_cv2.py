import os
import cv2
import base64
import asyncio
from socketio import AsyncServer
from app.torch.data import SAMPLE_VIDEOS_PATH
# torch module
from app.torch.market_customers_eval import async_mp4_track_with_yolo, async_webcam_track_with_yolo

async def stream_webcam(sio: AsyncServer, sid: str = None, controls: dict = None):
    if not sid: raise ValueError("Se requiere el SID del cliente a streamear")
    if controls is None: raise ValueError("Se requiere el diccionario de controles")

    async for annotated_frame in async_webcam_track_with_yolo():
        if controls[sid]["skip"]:
            print(f"Client {sid} requested skip, stopping stream.")
            break
        _, buffer = cv2.imencode(".jpg", annotated_frame)
        frame_b64 = base64.b64encode(buffer).decode("utf-8")
        await sio.emit("frame", {"image": frame_b64}, to=sid)
        await asyncio.sleep(0.05) 

async def stream_mp4(sio: AsyncServer, sid: str = None, controls: dict = None):
    if not sid: raise ValueError("Se requiere el SID del cliente a streamear")
    if controls is None: raise ValueError("Se requiere el diccionario de controles")

    controls[sid] = {"skip": False}

    while True:
        for video in os.listdir(SAMPLE_VIDEOS_PATH):
            video_path = os.path.join(SAMPLE_VIDEOS_PATH, video)
            if controls[sid]["skip"]:
                print(f"Client {sid} requested skip, stopping stream.")
                controls[sid]["skip"] = False
                continue
            async for annotated_frame in async_mp4_track_with_yolo(video_path):
                if controls[sid]["skip"]:
                    print(f"Client {sid} requested skip mid-video.")
                    controls[sid]["skip"] = False
                    break
                _, buffer = cv2.imencode(".jpg", annotated_frame)
                frame_b64 = base64.b64encode(buffer).decode("utf-8")
                await sio.emit("frame", {"image": frame_b64}, to=sid)
                await asyncio.sleep(0.05) 
        await asyncio.sleep(1)