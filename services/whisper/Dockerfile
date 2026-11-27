FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/models

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip ffmpeg ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m pip install --no-cache-dir \
    faster-whisper==1.1.1 \
    ctranslate2==4.6.0 \
    fastapi \
    uvicorn \
    python-multipart

RUN python3 -m pip install --no-cache-dir requests && python3 -m pip check && python3 -c "import requests; from faster_whisper import WhisperModel"

COPY server.py /app/server.py

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "server:app", \
     "--host", "0.0.0.0", "--port", "8000"]
