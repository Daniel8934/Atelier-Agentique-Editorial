import os
import tempfile
import shutil
from threading import Lock

import ctranslate2
from faster_whisper import WhisperModel
from fastapi import FastAPI, UploadFile, File, Form
from fastapi import HTTPException

app = FastAPI(title="Atelier Editorial - Whisper API")

MODEL_NAME = os.getenv("WHISPER_MODEL", "large-v3")
DEVICE = os.getenv("WHISPER_DEVICE", "cuda")
COMPUTE_TYPE = os.getenv(
    "WHISPER_COMPUTE_TYPE", "int8_float32"
)

model = None
lock = Lock()


@app.on_event("startup")
def startup():
    global model

    supported = ctranslate2.get_supported_compute_types(DEVICE)
    print("Types de calcul disponibles :", supported)

    if COMPUTE_TYPE not in supported:
        raise RuntimeError("Type de calcul incompatible")

    model = WhisperModel(
        MODEL_NAME,
        device=DEVICE,
        compute_type=COMPUTE_TYPE
    )


@app.get("/health")
def health():
    if model is None:
        raise HTTPException(503, "Modele non charge")

    return {
        "status": "ok",
        "model": MODEL_NAME,
        "device": DEVICE,
        "compute_type": COMPUTE_TYPE
    }


@app.get("/v1/models")
def models():
    return {
        "object": "list",
        "data": [
            {"id": MODEL_NAME, "object": "model"}
        ]
    }


@app.post("/v1/audio/transcriptions")
def transcribe(
    file: UploadFile = File(...),
    model: str = Form("large-v3"),
    language: str = Form(None)
):
    if model != MODEL_NAME:
        raise HTTPException(400, "Modele non disponible")

    path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".audio", delete=False
        ) as tmp:
            path = tmp.name
            shutil.copyfileobj(file.file, tmp)

        with lock:
            segments, info = globals()["model"].transcribe(
                path,
                language=language or None,
                beam_size=5,
                vad_filter=True
            )

            result = [
                {
                    "start": s.start,
                    "end": s.end,
                    "text": s.text.strip()
                }
                for s in segments
            ]

        return {
            "text": " ".join(s["text"] for s in result),
            "language": info.language,
            "segments": result
        }

    finally:
        file.file.close()

        if path and os.path.exists(path):
            os.unlink(path)
