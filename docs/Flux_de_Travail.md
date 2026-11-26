# Flux de Travail de l'Atelier Agentique Éditorial

Ce document décrit la méthode de travail pas à pas pour utiliser votre interface SaaS privée et piloter vos projets éditoriaux.

---

## 🚀 Étape 1 : Ingestion & Profilage
**Rôle :** Transformer la matière brute en matière structurée.

*   **Action :** Déposez vos fichiers (PDF, MP4, MP3) dans le dossier `/data`.
*   **Interface :** Cliquez sur le bouton **"Lancer l'Atelier"** du premier bloc.
*   **Ce que l'IA fait :** 
    *   Transcription (via Whisper local) ou extraction PDF.
    *   Identification contextuelle des locuteurs (Qui est qui ?).
    *   Création d'un premier glossaire technique.
*   **Votre Rôle (Validation) :** Un formulaire s'ouvre dans n8n. Vous confirmez ou corrigez l'identité des intervenants détectés.

---

## 🧠 Étape 2 : Architecture Éditoriale
**Rôle :** Extraire la substance et bâtir la structure narrative.

*   **Interface :** Cliquez sur le bouton **"Lancer l'Atelier"** du deuxième bloc.
*   **Ce que l'IA fait :**
    *   **Analyse Dialectique :** Repérage des contradictions, des chiffres clés et des "trous logiques".
    *   **Stratégie Narrative :** Proposition d'un arc narratif (le mouvement du texte).
    *   **Planification :** Génération d'un plan détaillé avec renvois précis aux sources.
*   **Votre Rôle (Expertise) :** Vous examinez le plan dans n8n. Vous y insufflez votre angle éditorial et validez la structure. 
*   **Livrable :** Le workflow génère votre `DOSSIER_TRAVAIL_FINAL.md`.

> ✍️ **PHASE HUMAINE :** C'est ici que vous rédigez votre manuscrit. Vous utilisez le dossier de travail comme base et vous apportez votre style, votre rythme et votre sensibilité littéraire.

---

## 🔍 Étape 3 : Audit & Finition
**Rôle :** Garantir la fiabilité factuelle et la cohérence finale.

*   **Interface :** Une fois votre rédaction terminée, cliquez sur le bouton **"Lancer l'Atelier"** du troisième bloc.
*   **Ce que l'IA fait :**
    *   **Comparaison Factuelle :** Vérifie que votre texte ne déforme pas les données de la source originale.
    *   **Contrôle de Cohérence :** S'assure que le ton est harmonisé et que les arguments se tiennent de bout en bout.
    *   **Rapport de Traçabilité :** Liste les points de vigilance éventuels.
*   **Votre Rôle (Jugement Critique) :** Vous lisez le rapport d'audit et procédez aux ultimes ajustements si nécessaire.

---

## 💡 Résumé des responsabilités

| Phase | Intelligence Artificielle | Expertise Humaine (VOUS) |
| :--- | :--- | :--- |
| **Logistique** | Transcription et Indexation | Vérification des identités |
| **Analyse** | Logique, failles et données | Stratégie et angle d'attaque |
| **Création** | *Support structurel* | **Rédaction littéraire et style** |
| **Qualité** | Comparaison factuelle | Jugement critique final |
