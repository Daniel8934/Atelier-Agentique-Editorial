# Guide de Mise en Service Technique

Ce document détaille les étapes indispensables pour activer votre plateforme **Atelier Agentique Éditorial** après l'installation des fichiers. Suivez cet ordre rigoureusement.

---

## 🧠 Étape 1 : Activation du "Cerveau" (Dify)

L'interface web ne peut pas fonctionner si les agents Dify ne sont pas prêts à répondre.

1.  Ouvrez votre interface **Dify** (généralement `http://localhost/`).
2.  Allez dans **"Exploration"** ou **"Apps"** et cliquez sur **"Importer un DSL"**.
3.  Importez successivement les 4 fichiers situés dans `workflows/Dify/`.
4.  **Crucial :** Pour chaque application importée :
    *   Allez dans l'onglet **"API Access"**.
    *   Cliquez sur **"Générer une clé API"**.
    *   Copiez et conservez précieusement ces 4 clés (Atelier 1, 2, 3 et 4).

---

## ⚡ Étape 2 : Configuration du "Système Nerveux" (n8n)

n8n doit savoir comment parler à Dify.

1.  Ouvrez votre interface **n8n**.
2.  Importez les 3 fichiers `.json` situés dans `workflows/n8n/`.
3.  **Lien avec Dify :** Dans chaque workflow n8n, repérez les nœuds **"HTTP Request"** (ceux qui appellent Dify) :
    *   Dans l'en-tête (Header) `Authorization`, remplacez le texte factice par `Bearer <VOTRE_CLÉ_API_DIFY>`.
4.  Activez les workflows en cliquant sur le bouton **"Active"** en haut à droite dans n8n.

---

## 👂 Étape 3 : Lancement de l'Oreille (Whisper Local)

Pour traiter les vidéos et l'audio sur votre carte graphique de 8 Go :

1.  Lancez le serveur Whisper via Docker :
    ```bash
    docker run -d --gpus all -p 8000:8000 fedirz/faster-whisper-server:latest-cuda
    ```
2.  Vérifiez qu'il tourne bien sur `http://localhost:8000`.

---

## 🖥️ Étape 4 : Lancement du Cockpit (Interface Web)

Une fois que les moteurs (Dify) et la plomberie (n8n) sont prêts, lancez l'interface :

1.  Ouvrez un terminal :
    ```bash
    cd ~/projets-agentiques/Atelier-Agentique-Editorial/interface
    source venv/bin/activate
    python3 app.py
    ```
2.  Ouvrez votre navigateur sur [http://localhost:5000](http://localhost:5000).

---

## 🔗 Étape Finale : La "Soudure" (Webhooks)

Pour que les boutons de votre interface web déclenchent réellement les actions dans n8n :

1.  Dans n8n, récupérez l'**URL de Webhook** de chaque workflow (Atelier 1, 2 et 3).
2.  Ouvrez `interface/templates/index.html`.
3.  Remplacez les fonctions `alert(...)` par un appel API vers ces URLs.

*(Si vous n'êtes pas à l'aise avec cette dernière étape, demandez-moi de le faire une fois que vous avez vos URLs n8n).*
