import os
import secrets
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request, jsonify, send_from_directory, session, abort

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32)
app.config.update(MAX_CONTENT_LENGTH=512 * 1024 * 1024, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Strict')
ROOT = Path(os.environ.get('EDITORIAL_DATA_DIR', str(Path.home() / 'projets-agentiques/Atelier-Agentique-Editorial/data'))).resolve()
FOLDERS = {'inbox':'01_inbox','temp':'02_temp','transcriptions':'03_transcriptions','mandats':'04_mandats','manuscrits':'05_manuscrits','audits':'06_audits','archives':'07_archives'}
MEDIA = {'.pdf','.mp3','.wav','.m4a','.aac','.flac','.ogg','.opus','.wma','.mp4','.mkv','.mov','.webm','.avi','.m4v'}

def folder(key):
    p = ROOT / FOLDERS[key]
    if p.is_symlink() or p.resolve().parent != ROOT:
        raise ValueError('Répertoire non autorisé')
    return p

def form_url(key):
    url = os.environ.get(key, '')
    p = urlparse(url)
    return url if p.scheme in ('http','https') and p.hostname and not p.username and not p.password else ''

@app.get('/')
def home():
    session.setdefault('csrf', secrets.token_hex(32))
    return render_template('index.html', csrf=session['csrf'], studio=form_url('N8N_STUDIO_FORM_URL'), audit=form_url('N8N_AUDIT_FORM_URL'))

@app.post('/api/upload/<kind>')
def upload(kind):
    if not session.get('csrf') or not secrets.compare_digest(request.headers.get('X-CSRF-Token',''), session['csrf']):
        abort(403)
    if kind not in ('inbox','manuscrits'):
        abort(404)
    f = request.files.get('file')
    name = f.filename if f else ''
    # Match the conservative ASCII names accepted by the n8n workflows.
    import re
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,180}', name) or '..' in name:
        return jsonify(error='Nom invalide : utiliser lettres ASCII, chiffres, tirets et underscores.'), 400
    if Path(name).suffix.lower() not in (MEDIA if kind=='inbox' else {'.md'}):
        return jsonify(error='Extension non autorisée.'), 400
    tmp = None
    try:
        dest = folder(kind); dest.mkdir(parents=True, exist_ok=True)
        staging = folder('temp'); staging.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=staging, delete=False) as out:
            tmp = Path(out.name); f.save(out)
        if tmp.stat().st_size == 0:
            return jsonify(error='Fichier vide.'), 400
        # Atomic publication without overwriting a source, on the same filesystem.
        os.link(tmp, dest / name)
        return jsonify(message='Fichier déposé. Le traitement dépend du workflow n8n actif.', filename=name), 201
    except FileExistsError:
        return jsonify(error='Ce fichier existe déjà.'), 409
    except (OSError, ValueError):
        return jsonify(error='Écriture impossible. Vérifier les permissions et le volume partagé.'), 500
    finally:
        if tmp is not None: tmp.unlink(missing_ok=True)

@app.get('/api/files')
def files():
    result = {}
    for key in ('transcriptions','mandats','manuscrits','audits','archives'):
        try:
            p=folder(key)
            result[key]=[{'name':x.name,'size':x.stat().st_size} for x in sorted(p.iterdir()) if x.is_file() and not x.is_symlink() and x.suffix.lower()=='.md'] if p.exists() else []
        except (OSError, ValueError):
            return jsonify(error='Lecture des répertoires impossible.'), 500
    return jsonify(result)

@app.get('/files/<kind>/<name>')
def download(kind,name):
    if kind not in ('transcriptions','mandats','manuscrits','audits','archives') or Path(name).name != name or Path(name).suffix.lower() != '.md': abort(404)
    p=folder(kind)
    if (p/name).is_symlink(): abort(404)
    return send_from_directory(p,name,as_attachment=True)

def probe(url):
    try:
        with urlopen(url,timeout=2) as r: return 'Accessible' if 200 <= r.status < 300 else 'À vérifier'
    except Exception: return 'Non confirmé'

@app.get('/api/status')
def status():
    urls={'n8n':os.environ.get('N8N_HEALTH_URL','http://localhost:5678/healthz'),'Dify':os.environ.get('DIFY_HEALTH_URL','http://127.0.0.1/console/api/system-features'),'Whisper':os.environ.get('WHISPER_HEALTH_URL','http://localhost:8000/health')}
    with ThreadPoolExecutor(max_workers=3) as pool:
        result=dict(zip(urls,pool.map(probe,urls.values())))
    result['Stockage']='Accessible en écriture' if ROOT.is_dir() and os.access(ROOT,os.W_OK) else 'À configurer'
    return jsonify(result)

@app.after_request
def headers(response):
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Cache-Control']='no-store'
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['X-Frame-Options']='DENY'
    response.headers['Content-Security-Policy']="default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    return response


# CONFIGURATION_SYSTEME_EDITORIAL
from flask import jsonify as system_jsonify

_original_system_status = app.view_functions["status"]

def editorial_system_status():
    response = app.make_response(_original_system_status())
    data = response.get_json()

    if not isinstance(data, dict):
        return response

    data["Instance Dify"] = "1.20.0"
    data["Moteur Cloud"] = "Gemini 3.1 Flash-Lite"

    return system_jsonify(data), response.status_code

app.view_functions["status"] = editorial_system_status

if __name__=='__main__':
    app.run(host='127.0.0.1',port=int(os.environ.get('PORT','5000')),debug=False)
