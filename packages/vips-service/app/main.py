from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from app.controller.socketio_cv2 import socket_app
from app.config import Config

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.mount(Config.SOCKETIO_PATH, socket_app)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=9000, reload=True)