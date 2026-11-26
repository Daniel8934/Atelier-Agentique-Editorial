# Guide de Fonctionnement des Workflows n8n

Ce document explique le rôle et le fonctionnement des trois workflows n8n qui constituent le "système nerveux" de l'**Atelier Agentique Éditorial**.

---

## 1. L'Ingesteur Audiovisuel (Local)
**Objectif :** Transformer la matière brute (vidéo/audio) en texte exploitable tout en garantissant une confidentialité totale.

### Fonctionnement détaillé :
1.  **Déclencheur (Trigger) :** Le workflow surveille en permanence le dossier `/data`. Dès qu'un fichier est ajouté, il s'active automatiquement.
2.  **Traitement FFmpeg :** Une commande système extrait la piste sonore et la convertit en format MP3 (16kHz, mono). Cette étape est cruciale pour optimiser la vitesse de transcription.
3.  **Transcription Whisper :** L'audio est envoyé à votre serveur **Whisper local** (via Docker). Le texte est généré sans jamais transiter par un serveur externe.
4.  **Sortie :** Le workflow enregistre un fichier `.md` (Markdown) dans le dossier `/data`. Ce fichier devient la "Source de Vérité" pour tout le processus éditorial.

**Quand l'utiliser ?** Dès réception de fichiers sources multimédias de la part d'un client.

---

## 2. Le Studio Éditorial (Orchestrateur)
**Objectif :** Piloter la phase de création, de l'identification des voix jusqu'à l'élaboration du plan détaillé.

### Fonctionnement détaillé :
1.  **Initialisation :** Vous lancez le workflow via un formulaire n8n en indiquant le nom du fichier texte à traiter.
2.  **Appel Atelier 1 (Profileur) :** n8n envoie le texte à Dify. L'IA identifie les locuteurs (ex: SPEAKER_00 = Jean).
3.  **Validation Locuteurs (Point d'Arrêt) :** Le workflow s'arrête et vous présente un formulaire. Vous validez ou corrigez les noms. Une fois validé, n8n normalise tout le document avec les vrais noms.
4.  **Appel Ateliers 2 & 3 (Analyse & Plan) :** n8n sollicite les agents Dify pour extraire les arguments, détecter les contradictions et proposer un plan narratif structuré.
5.  **Révision du Plan (Point d'Arrêt) :** Un second formulaire vous présente l'analyse dialectique et le plan. Vous pouvez modifier le plan directement pour qu'il corresponde à votre intention d'auteur.
6.  **Sortie :** Un fichier `DOSSIER_TRAVAIL_FINAL.md` est généré. C'est votre cahier des charges pour la phase de rédaction.

**Quand l'utiliser ?** Pour transformer une transcription brute en une structure éditoriale solide et cohérente.

---

## 3. L'Audit de Finition
**Objectif :** Garantir la qualité finale et la traçabilité avant livraison au client.

### Fonctionnement détaillé :
1.  **Entrée :** Via un formulaire, vous fournissez le nom du fichier source original et le nom de votre manuscrit final (celui que vous avez rédigé).
2.  **Appel Atelier 4 (Réviseur) :** n8n transmet les deux textes à l'agent Dify (Gemini 1.5 Pro).
3.  **Analyse Comparative :** L'IA compare systématiquement les deux versions pour détecter :
    *   Les erreurs factuelles ou les chiffres altérés.
    *   Les glissements de sens ou les oublis d'arguments clés.
    *   Les ruptures de cohérence ou d'harmonisation terminologique.
4.  **Sortie :** Un fichier `RAPPORT_AUDIT_FINAL.md` est créé. Il liste chaque point de vigilance pour vous permettre une dernière correction chirurgicale.

**Quand l'utiliser ?** Juste avant d'exporter votre version finale pour le client, afin de garantir un travail "zéro défaut".
