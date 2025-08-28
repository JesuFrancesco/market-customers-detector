import asyncio
import base64
import cv2
import os
from app.torch.data import SAMPLE_VIDEOS_PATH
from socketio import AsyncServer

# == Torch module
from app.torch.face_embedding_eval import async_webcam_face_recognition, async_video_face_recognition

async def stream_webcam(sio: AsyncServer, sid: str = None, controls: dict = None):
    if not sid: raise ValueError("Se requiere el SID del cliente a streamear")
    if controls is None: raise ValueError("Se requiere el diccionario de controles")

    async for annotated_frame in async_webcam_face_recognition():
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

    while True:
        for video in os.listdir(SAMPLE_VIDEOS_PATH):
            video_path = os.path.join(SAMPLE_VIDEOS_PATH, video)
            async for annotated_frame in async_video_face_recognition(video_path=video_path):
                if controls[sid]["skip"]:
                    print(f"Client {sid} requested skip, stopping stream.")
                    break
                _, buffer = cv2.imencode(".jpg", annotated_frame)
                frame_b64 = base64.b64encode(buffer).decode("utf-8")
                await sio.emit("frame", {"image": frame_b64}, to=sid)
                await asyncio.sleep(0.05) 
            