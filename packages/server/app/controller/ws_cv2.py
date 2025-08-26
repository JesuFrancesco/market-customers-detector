import socketio
from packages.server.app.service.ws_cv2 import stream_webcam

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)
socket_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)
    # Start background task
    sio.start_background_task(lambda: stream_webcam(sio))

@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)

print("module finished")