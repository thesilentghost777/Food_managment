FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements_docker.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY . .

EXPOSE 5000

# Pas besoin de CMD ici car défini dans docker-compose.yml
