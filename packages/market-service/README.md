# market-service

## Information

Use the [videos](./app/torch/data/videos/) directory to create folders with different ids

## Commands

- Start server

```sh
python -m app.main
```

- Probar YOLO en local

```sh
# Usar WebCam
python -m app.torch.market_customers_eval --webcam

# Usar video MP4
python -m app.torch.market_customers_eval --mp4

# Ayuda
python -m app.torch.market_customers_eval --help
```

## References

- Yolov11 (COCO): https://github.com/ultralytics/assets
