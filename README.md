# Atelier Agentique Éditorial

## 🌟 Vision du Projet
L'**Atelier Agentique Éditorial** est une plateforme de travail hybride conçue pour maximiser la production intellectuelle et éditoriale de haute qualité. Elle repose sur le principe du **"Human-in-the-loop"** : l'intelligence artificielle prend en charge la gestion de la complexité, la logistique des données et l'analyse structurelle, libérant ainsi l'expert humain pour les tâches à haute valeur ajoutée (style, nuance, jugement critique et sensibilité littéraire).

## 🏗️ Architecture Technique
- **n8n** : Le système nerveux central. Orchestre les flux, gère les fichiers, les appels API et les points de validation humaine.
- **Dify (v1.19.0)** : Le moteur d'intelligence. Héberge des agents spécialisés organisés en workflows modulaires.
- **Whisper / WhisperX** : L'oreille de la plateforme pour la transcription et la diarisation (identification des locuteurs).
- **OBS Studio** : Interface de capture pour les briefings vocaux et les retours d'expertise.

## 🛠️ Les 4 Ateliers de Production

### 1. Atelier : Profileur & Indexeur
- **Rôle** : Préparation de la matière brute.
- **Fonctions** : Identification des intervenants (Diarisation contextuelle), création de glossaires techniques et indexation des sources dans la base de connaissances.

### 2. Atelier : Analyste Dialectique
- **Rôle** : Analyse de fond et extraction de substance.
- **Fonctions** : Repérage des arguments clés, détection des contradictions, identification des "trous" logiques et des redondances.

### 3. Atelier : Architecte Éditorial
- **Rôle** : Structuration et mise en récit.
- **Fonctions** : Génération de plans détaillés avec renvois aux sources, proposition de "narrative arcs" et organisation thématique.

### 4. Atelier : Réviseur-Comparateur
- **Rôle** : Audit, traçabilité et finition.
- **Fonctions** : Comparaison de versions, vérification de la cohérence entre chapitres, harmonisation terminologique et production de grilles d'analyse.

## 📂 Structure du Projet
- `/workflows` : Fichiers YAML des configurations Dify.
- `/prompts` : Bibliothèque des prompts "maîtres" pour chaque agent.
- `/scripts` : Utilitaires Python pour le traitement de données (FFmpeg, WhisperX, etc.).
- `/docs` : Documentation méthodologique et guides d'utilisation.
- `/data` : Espace de transit pour les documents de travail (transcriptions, PDF).

## ✒️ Valeur Ajoutée Humaine
La plateforme ne remplace pas l'auteur. Elle fournit une base clinique sur laquelle l'expert apporte :
- L'angle éditorial et la clarté pédagogique.
- Le rythme et la qualité littéraire de la langue française.
- Le respect absolu de l'intention d'origine.
- Le jugement critique et les recommandations stratégiques.
