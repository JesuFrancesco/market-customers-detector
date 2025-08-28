import asyncio
import cv2
import base64
from socketio import AsyncServer

# == Torch module
from app.torch.face_embedding_eval import async_webcam_face_recognition

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

    print("Not implemented !!!")
    