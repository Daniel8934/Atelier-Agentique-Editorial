#!/bin/bash

echo "🛑 Arrêt de toutes les instances Dify..."

# Instance Test / Officielle
if [ -d "$HOME/dify/docker" ]; then
    echo "--- Arrêt de Dify (Standard) ---"
    cd $HOME/dify/docker && docker compose down
fi

# Instance Préparation 1.19
if [ -d "$HOME/dify-1.19-preparation/docker" ]; then
    echo "--- Arrêt de Dify 1.19 (Préparation) ---"
    cd $HOME/dify-1.19-preparation/docker && docker compose down
fi

echo "🧹 Nettoyage des ressources Docker résiduelles..."
docker network prune -f
docker container prune -f

echo "🚀 Relance de l'instance Dify 1.19 uniquement..."
cd $HOME/dify-1.19-preparation/docker && docker compose up -d

echo "✅ Serveur assaini. Seul Dify 1.19 est actif."
docker compose ps
