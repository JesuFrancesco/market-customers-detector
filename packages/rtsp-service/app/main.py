from fastapi import FastAPI
import subprocess
import signal
import asyncio

async def lifespan(_: FastAPI):
    start_stream()

    yield
    # Cleanup code on shutdown
    if FFMPEG_PROCESS is not None:
        FFMPEG_PROCESS.send_signal(signal.SIGINT)
        await asyncio.sleep(1)  # Give some time for the process to terminate

app = FastAPI(lifespan=lifespan)

FFMPEG_PROCESS = None
VIDEO_PATH = r"C:\Users\Jesu\Documents\__Documentos\dev\final-cloud-computing\packages\market-service\app\torch\data\videos\sample_video1.mp4"
RTSP_URL = "rtsp://localhost:8554/mystream"


@app.post("/start_stream")
def start_stream():
    global FFMPEG_PROCESS
    if FFMPEG_PROCESS is not None:
        return {"status": "already running", "url": RTSP_URL}

    # ffmpeg command: loop video and push to RTSP
    cmd = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",   # loop forever
        "-i", VIDEO_PATH,
        "-c:v", "libx264",
        "-f", "rtsp",
        RTSP_URL
    ]

    FFMPEG_PROCESS = subprocess.Popen(cmd)
    return {"status": "started", "url": RTSP_URL}


@app.post("/stop_stream")
def stop_stream():
    global FFMPEG_PROCESS
    if FFMPEG_PROCESS is not None:
        FFMPEG_PROCESS.send_signal(signal.SIGINT)
        FFMPEG_PROCESS = None
        return {"status": "stopped"}
    return {"status": "not running"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)