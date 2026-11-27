import os
import tempfile
import shutil
from threading import Lock

import ctranslate2
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi import HTTPException

app = FastAPI(title="Atelier Editorial - Whisper API")

MODEL_NAME = os.getenv("WHISPER_MODEL", "base")
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
    model: str = Form("base"),
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

        sample_rate = 16000
        chunk_size = 15 * sample_rate
        overlap = 2 * sample_rate
        step = chunk_size - overlap

        audio = decode_audio(path, sampling_rate=sample_rate)

        if len(audio) == 0:
            raise HTTPException(400, "Audio vide")

        result = []
        detected_language = language or None
        offset = 0

        with lock:
            while offset < len(audio):
                end = min(offset + chunk_size, len(audio))
                chunk = audio[offset:end]

                segments, info = globals()["model"].transcribe(
                    chunk,
                    language=detected_language,
                    beam_size=5,
                    vad_filter=False,
                    word_timestamps=True,
                    condition_on_previous_text=False
                )

                detected_language = info.language

                left = (
                    0 if offset == 0
                    else overlap / (2 * sample_rate)
                )

                right = len(chunk) / sample_rate

                if end < len(audio):
                    right -= overlap / (2 * sample_rate)

                for segment in segments:
                    words = [
                        w for w in (segment.words or [])
                        if left <= (w.start + w.end) / 2 < right
                    ]

                    if words:
                        text = "".join(w.word for w in words).strip()

                        if text:
                            result.append({
                                "start": round(
                                    offset / sample_rate
                                    + words[0].start, 3
                                ),
                                "end": round(
                                    min(
                                        len(audio) / sample_rate,
                                        offset / sample_rate
                                        + words[-1].end
                                    ), 3
                                ),
                                "text": text
                            })

                    elif not segment.words:
                        middle = (segment.start + segment.end) / 2

                        if left <= middle < right and segment.text.strip():
                            result.append({
                                "start": round(
                                    offset / sample_rate + segment.start, 3
                                ),
                                "end": round(
                                    min(
                                        len(audio) / sample_rate,
                                        offset / sample_rate + segment.end
                                    ), 3
                                ),
                                "text": segment.text.strip()
                            })

                print(
                    f"Fenetre : {offset / sample_rate:.2f}"
                    f" - {end / sample_rate:.2f} s",
                    flush=True
                )

                if end == len(audio):
                    break

                offset += step

        result.sort(key=lambda s: s["start"])

        if not result:
            raise HTTPException(422, "Aucune parole transcrite")

        return {
            "text": " ".join(s["text"] for s in result),
            "language": detected_language,
            "segments": result
        }

    finally:
        file.file.close()

        if path and os.path.exists(path):
            os.unlink(path)
