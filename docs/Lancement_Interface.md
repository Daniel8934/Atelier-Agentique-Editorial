# Guide de Lancement de l'Interface Web

Ce document explique comment démarrer et accéder à l'interface SaaS privée de l'**Atelier Agentique Éditorial** sur votre Ubuntu Server Pro.

## 🛠️ Première Installation (Configuration de l'environnement)

Comme Ubuntu protège désormais l'installation globale des paquets Python, nous utilisons un environnement virtuel (`venv`). Ces étapes ne sont à faire **qu'une seule fois**.

1.  **Naviguer dans le dossier interface :**
    ```bash
    cd ~/projets-agentiques/Atelier-Agentique-Editorial/interface
    ```

2.  **Créer l'environnement virtuel :**
    ```bash
    python3 -m venv venv
    ```

3.  **Activer l'environnement :**
    ```bash
    source venv/bin/activate
    ```

4.  **Installer Flask :**
    ```bash
    pip install flask
    ```

---

## 🚀 Lancement Quotidien

Chaque fois que vous souhaitez ouvrir votre interface :

1.  **Ouvrir un terminal et lancer le serveur :**
    ```bash
    cd ~/projets-agentiques/Atelier-Agentique-Editorial/interface
    source venv/bin/activate
    python3 app.py
    ```

2.  **Accéder à l'interface dans votre navigateur :**
    - Si vous êtes sur le serveur : [http://localhost:5000](http://localhost:5000)
    - Si vous êtes sur un autre appareil : `http://<IP_DU_SERVEUR>:5000`
      *(Utilisez `hostname -I` pour trouver l'IP du serveur).*

---

## 🛑 Arrêter l'interface

Pour arrêter le serveur Web, faites simplement **`CTRL + C`** dans le terminal où il est lancé.
Pour quitter l'environnement virtuel, vous pouvez taper `deactivate`.

---

## 🔒 Sécurité & GitHub
Le dossier `venv/` créé est automatiquement ignoré par votre fichier `.gitignore` afin de ne pas polluer votre répertoire GitHub.
