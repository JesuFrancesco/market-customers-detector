# rtsp-service

FastAPI + RTSP server to simulate IP camera

## Prerequisites

- ffmpeg
- [Latest mediamtx binary](https://github.com/bluenviron/mediamtx/releases/latest)

## Commands

```sh
# 1. Start the mediamtx process
./lib/mediamtx.exe

# 2. Run the FastAPI producer
python -m app.main

# 3. See the stream
ffplay rtsp://localhost:8554/mystream
```
