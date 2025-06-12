#!/bin/bash

# Nom du projet
PROJECT_NAME="."

# Créer les dossiers principaux
mkdir -p $PROJECT_NAME/app/routes
mkdir -p $PROJECT_NAME/app/services
mkdir -p $PROJECT_NAME/migrations

# Fichiers de base
touch $PROJECT_NAME/app/__init__.py
touch $PROJECT_NAME/app/models.py
touch $PROJECT_NAME/app/config.py

# Fichiers routes
touch $PROJECT_NAME/app/routes/__init__.py
touch $PROJECT_NAME/app/routes/person_routes.py
touch $PROJECT_NAME/app/routes/food_routes.py
touch $PROJECT_NAME/app/routes/allergy_routes.py

# Fichiers services
touch $PROJECT_NAME/app/services/__init__.py
touch $PROJECT_NAME/app/services/utils.py
touch $PROJECT_NAME/app/services/recommendation.py

# Fichiers à la racine
touch $PROJECT_NAME/run.py
touch $PROJECT_NAME/.env
touch $PROJECT_NAME/requirements.txt
touch $PROJECT_NAME/README.md
touch $PROJECT_NAME/.gitignore

# Écrire un .gitignore de base
cat <<EOL > $PROJECT_NAME/.gitignore
__pycache__/
*.pyc
.env
instance/
.mypy_cache/
EOL

# Affichage de confirmation
echo "✅ Structure du projet Flask backend créée dans ./$PROJECT_NAME"

