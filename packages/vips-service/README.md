# vips-service

## Information

Use the [gallery](./app/torch/data/gallery/) directory to create folders with different ids

## Commands

- Start server

```sh
python -m app.main
```

- Probar modelo ArcFace en local

```sh
# WebCam
python -m app.torch.face_embedding_eval --webcam
```

## References

- Yolov8-Face: https://github.com/lindevs/yolov8-face
- InsightFace: https://github.com/deepinsight/insightface
- Antelopev2 (ArcFaceONNX): https://huggingface.co/immich-app/antelopev2
