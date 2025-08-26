import socketio
from app.service.ws_cv2 import stream_mp4
# from app.service.ws_cv2 import stream_webcam

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)
socket_app = socketio.ASGIApp(sio)

events = {}
controls = {}

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)
    # Start background task
    controls[sid] = {"skip": False}
    task = sio.start_background_task(stream_mp4, sio, sid, controls)
    # task = sio.start_background_task(stream_webcam, sio, sid, controls)
    events[sid] = task

@sio.event
async def control(sid, data):
    action = data.get("action")
    if action == "skip":
        controls[sid]["skip"] = True
        await sio.emit("message", {"status": "skipping video"}, to=sid)

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)
    task = events.get(sid)
    if task:
        task.cancel()
        del events[sid]
