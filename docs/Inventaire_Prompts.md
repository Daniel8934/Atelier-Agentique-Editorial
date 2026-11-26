# Inventaire des Prompts Intégrés

Ce document répertorie les prompts professionnels déjà configurés à l'intérieur des workflows Dify de l'**Atelier Agentique Éditorial**. Chaque prompt a été conçu pour maximiser la pertinence des réponses tout en minimisant la consommation de tokens avec **Gemini 1.5 Flash/Pro**.

---

## 🏗️ Atelier 1 : Profileur & Indexeur
*Fichier : `workflows/Dify/Atelier_1_Profileur_Indexeur.yml`*

### 1. Agent Profileur (Stratégie A)
- **Rôle :** Expert en analyse de discours.
- **Mission :** Identifier l'identité ou le rôle des locuteurs (`SPEAKER_XX`) en analysant les salutations, le contexte et les présentations dans les 5000 premiers caractères.
- **Format de sortie :** JSON strict pour permettre une automatisation via script Code.

### 2. Générateur de Glossaire
- **Rôle :** Terminologue expert.
- **Mission :** Extraire les concepts clés, acronymes et termes techniques.
- **Format de sortie :** Tableau Markdown avec définitions contextuelles.

---

## ⚖️ Atelier 2 : Analyste Dialectique
*Fichier : `workflows/Dify/Atelier_2_Analyste_Dialectique.yml`*

### 1. Extracteur d'Arguments & Données
- **Rôle :** Analyste de preuves factuelles.
- **Mission :** Isoler les thèses principales, les chiffres, les dates et les faits vérifiables.
- **Style :** Clinique et précis, sans interprétation.

### 2. Auditeur de Logique (Analyse Dialectique)
- **Rôle :** Expert en rhétorique et logique.
- **Mission :** Détecter les contradictions internes, les trous logiques (affirmations sans preuves) et les points de divergence entre les intervenants.

---

## 📐 Atelier 3 : Architecte Éditorial
*Fichier : `workflows/Dify/Atelier_3_Architecte_Editorial.yml`*

### 1. Stratège Narratif (Vision)
- **Rôle :** Architecte de contenu.
- **Mission :** Définir l'arc narratif global, le mouvement logique du futur texte, ainsi que le ton et le rythme conseillés.

### 2. Concepteur de Plan (Structure)
- **Rôle :** Maquettiste de structure complexe.
- **Mission :** Créer un plan détaillé (Titres/Sous-titres) où chaque section comporte un résumé et un renvoi précis aux sources de la matière brute.

---

## 🔍 Atelier 4 : Réviseur-Comparateur
*Fichier : `workflows/Dify/Atelier_4_Reviseur_Comparateur.yml`*

### 1. Expert en Traçabilité (Comparaison)
- **Rôle :** Auditeur de conformité éditoriale.
- **Mission :** Comparer le manuscrit final à la source brute pour détecter les écarts de faits, les glissements de sens ou les changements de ton non désirés.

### 2. Réviseur de Cohérence Globale
- **Rôle :** Réviseur linguistique et logique de haut niveau.
- **Mission :** Vérifier l'harmonisation terminologique sur l'ensemble du document et s'assurer que la conclusion répond aux promesses de l'introduction.
