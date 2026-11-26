#!/bin/bash

# ==============================================================================
# Script de Sauvegarde Automatisée - Atelier Agentique Éditorial
# Rétention : 30 dernières sauvegardes
# ==============================================================================

# Configuration des chemins
SOURCE_DIR="/home/daniel/projets-agentiques/Atelier-Agentique-Editorial"
BACKUP_BASE_DIR="/run/media/daniel/clients"
BACKUP_DEST_DIR="$BACKUP_BASE_DIR/backups_atelier_agentique"
RETENTION_COUNT=30

# Génération du nom de fichier avec horodatage
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILE_NAME="backup_atelier_$DATE.tar.gz"

# 1. Vérifier si le disque "clients" est monté
if [ ! -d "$BACKUP_BASE_DIR" ]; then
    echo "❌ Erreur : Le disque 'clients' n'est pas monté sur $BACKUP_BASE_DIR"
    exit 1
fi

# 2. Créer le dossier de destination s'il n'existe pas
mkdir -p "$BACKUP_DEST_DIR"

# 3. Créer l'archive compressée
echo "🚀 Démarrage de la sauvegarde de l'Atelier..."
tar -czf "$BACKUP_DEST_DIR/$FILE_NAME" \
    --exclude="*.log" \
    --exclude="node_modules" \
    --exclude="venv" \
    -C "$SOURCE_DIR" .

if [ $? -eq 0 ]; then
    echo "✅ Sauvegarde réussie : $FILE_NAME"
else
    echo "❌ Erreur lors de la compression."
    exit 1
fi

# 4. Rotation des sauvegardes (Garder seulement les 30 plus récentes)
echo "🧹 Nettoyage des anciennes sauvegardes (Rétention : $RETENTION_COUNT)..."

# Liste les fichiers par date (du plus ancien au plus récent), 
# exclut les 30 plus récents de la liste, et supprime le reste.
cd "$BACKUP_DEST_DIR" && ls -1tr backup_atelier_*.tar.gz 2>/dev/null | head -n -"$RETENTION_COUNT" | xargs -d '\n' rm -f --

echo "✨ Opération terminée avec succès."
