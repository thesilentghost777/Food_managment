#!/bin/bash
path="./"

# Parcours tous les fichiers du répertoire
for file in "$path"/* ; do
    # Vérifie si c'est un fichier régulier
    if [ -f "$file" ]; then
        cat "$file" >> requirements.txt
    fi
done
