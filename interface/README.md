# Atelier Agentique Éditorial — Interface locale

Installer : `python3 -m venv .venv`, puis `source .venv/bin/activate` et `pip install -r requirements.txt`.

Configurer dans le terminal (remplacer les deux URL de formulaire par les Production URLs copiées dans les nœuds Form Trigger n8n) :

```bash
export EDITORIAL_DATA_DIR="$HOME/projets-agentiques/Atelier-Agentique-Editorial/data"
export N8N_STUDIO_FORM_URL=''
export N8N_AUDIT_FORM_URL=''
export N8N_HEALTH_URL='http://localhost:5678/healthz'
export DIFY_HEALTH_URL='http://localhost/health'
export WHISPER_HEALTH_URL='http://localhost:8000/health'
mkdir -p "$EDITORIAL_DATA_DIR"/{01_inbox,02_temp,03_transcriptions,04_mandats,05_manuscrits,06_audits,07_archives}
python app.py
```

Ouvrir http://127.0.0.1:5000. Publier/activer les workflows n8n avant les tests. Les URL des formulaires doivent être accessibles depuis le navigateur. Le dossier temporaire et les dossiers de dépôt doivent être sur le même système de fichiers (publication atomique par lien dur). Les fichiers déposés ne sont pas écrasés. Les noms ASCII simples sont requis. Limite de requête : 512 Mio.

Les contrôles HTTP ne garantissent pas la disponibilité de Gemini ou du GPU ; adapter les URL de santé à l'installation. L'ingestion est asynchrone côté n8n ; le dépôt ne confirme pas la transcription. Les archives sont en lecture seule et ne recensent que les fichiers Markdown au premier niveau. Aucun appel direct Dify ni clé API côté navigateur.

Ce prototype est prévu pour un usage local mono-utilisateur, sans authentification utilisateur. Ne pas exposer sur Internet : ajouter authentification, HTTPS, serveur WSGI de production, permissions et protection des formulaires n8n. En accès distant, utiliser par exemple un tunnel SSH. Les vérifications de noms ne remplacent pas un contrôle du contenu des fichiers. Conserver les répertoires de données sous contrôle de l'utilisateur de service.
