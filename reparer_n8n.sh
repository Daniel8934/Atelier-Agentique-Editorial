#!/usr/bin/env bash
set -euo pipefail

PROJECT="$HOME/projets-agentiques/Atelier-Agentique-Editorial"
N8N_DIR="/opt/n8n"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP="$PROJECT/sauvegardes/n8n-$STAMP"

mkdir -p "$BACKUP"
chmod 700 "$BACKUP"

echo "===== SAUVEGARDE ====="

sudo cp "$N8N_DIR/compose.yaml" "$BACKUP/compose.yaml"
sudo chmod 600 "$BACKUP/compose.yaml"

IMAGE_ID="$(docker inspect n8n-n8n-1 --format '{{.Image}}')"

docker tag "$IMAGE_ID" atelier-n8n-base:2.47.7

echo "===== CREATION DES REPERTOIRES ====="

mkdir -p "$PROJECT/data"/{01_inbox,02_temp,03_transcriptions,04_mandats,05_manuscrits,06_audits,07_archives}

echo "===== DOCKERFILE PERSONNALISE ====="

sudo tee "$N8N_DIR/Dockerfile.atelier" >/dev/null <<'EOF'
FROM alpine:3.24 AS ffmpeg
RUN apk add --no-cache ffmpeg

FROM atelier-n8n-base:2.47.7

USER root

COPY --from=ffmpeg /usr/bin/ffmpeg /opt/ffmpeg/bin/ffmpeg
COPY --from=ffmpeg /usr/bin/ffprobe /opt/ffmpeg/bin/ffprobe
COPY --from=ffmpeg /usr/lib/ /opt/ffmpeg/lib/

ENV PATH="/opt/ffmpeg/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/ffmpeg/lib"

USER node
EOF

echo "===== CONFIGURATION COMPLEMENTAIRE ====="

sudo tee "$N8N_DIR/compose.atelier.yaml" >/dev/null <<EOF
services:
  n8n:
    image: atelier-n8n:2.47.7-ffmpeg
    build:
      context: .
      dockerfile: Dockerfile.atelier
    environment:
      NODES_EXCLUDE: '[]'
      N8N_RESTRICT_FILE_ACCESS_TO: "$PROJECT/data"
    volumes:
      - "$PROJECT/data:$PROJECT/data:rw"
EOF

echo "===== VALIDATION COMPOSE ====="

cd "$N8N_DIR"

docker compose \
  -f compose.yaml \
  -f compose.atelier.yaml \
  config --quiet

echo "===== CONSTRUCTION IMAGE ====="

docker compose \
  -f compose.yaml \
  -f compose.atelier.yaml \
  build n8n

echo "===== TEST FFMPEG AVANT REDEMARRAGE ====="

docker run --rm \
  --entrypoint ffmpeg \
  atelier-n8n:2.47.7-ffmpeg \
  -version

echo "===== SAUVEGARDE TERMINEE ====="

echo "Configuration sauvegardee dans : $BACKUP"
echo "Image personnalisee construite."
echo "Le conteneur n8n actuel n'a pas ete arrete."
