#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/projets-agentiques/Atelier-Agentique-Editorial/interface"

get_form_url() {
    local id="$1"
    local remote="/tmp/atelier-form-${id}-$$.json"
    local localfile

    localfile="$(mktemp)"

    if docker exec n8n-n8n-1 n8n export:workflow \
        --id="$id" --output="$remote" >&2 &&
       docker cp "n8n-n8n-1:$remote" "$localfile" >&2
    then
        python3 - "$localfile" <<'PY'
import json
import sys
from urllib.parse import quote

with open(sys.argv[1]) as f:
    data = json.load(f)

workflow = data[0] if isinstance(data, list) else data

for node in workflow.get("nodes", []):
    if node.get("type") == "n8n-nodes-base.formTrigger":
        params = node.get("parameters", {})
        path = (
            params.get("path")
            or params.get("options", {}).get("path")
            or node.get("webhookId")
        )
        if path and not path.startswith("="):
            print("http://localhost:5678/form/" + quote(path.strip("/"), safe="/"))
        break
PY
    fi

    docker exec n8n-n8n-1 rm -f "$remote" >/dev/null 2>&1 || true
    rm -f "$localfile"
}

export N8N_STUDIO_FORM_URL="$(get_form_url HrMNvG1WWY0B8q18)"
export N8N_AUDIT_FORM_URL="$(get_form_url 6xetdK3V30NHg8tL)"

export DIFY_HEALTH_URL="http://127.0.0.1/console/api/system-features"
export WHISPER_HEALTH_URL="http://127.0.0.1:8000/health"
export N8N_HEALTH_URL="http://127.0.0.1:5678/healthz"

echo "===== CONFIGURATION DE L'INTERFACE ====="
echo "Studio : ${N8N_STUDIO_FORM_URL:-NON CONFIGURE}"
echo "Audit  : ${N8N_AUDIT_FORM_URL:-NON CONFIGURE}"

source venv/bin/activate

exec python app.py
