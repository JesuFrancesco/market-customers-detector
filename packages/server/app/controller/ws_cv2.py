import socketio
from app.service.ws_cv2 import stream_webcam, stream_cv2

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)
socket_app = socketio.ASGIApp(sio)

events = {}

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)
    # Start background task
    task = sio.start_background_task(lambda: stream_cv2(sio))
    events[sid] = task

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)
    task = events.get(sid)
    if task:
        task.cancel()
        del events[sid]
