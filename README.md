# 🍽️ Application de Gestion Alimentaire et de Buffet

Une application web backend développée avec Flask pour la gestion d'informations alimentaires, la détection d'allergies, et la planification de repas, avec un focus sur les cuisines africaines.

## 📋 Table des Matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation et Démarrage](#installation-et-démarrage)
- [API Endpoints](#api-endpoints)
- [Tests avec Postman](#tests-avec-postman)
- [Structure du Projet](#structure-du-projet)
- [Pays Couverts](#pays-couverts)
- [Contribution](#contribution)

## 🎯 Aperçu

Cette application s'inscrit dans le cadre des Objectifs de Développement Durable (ODD 2 - Faim Zéro et ODD 3 - Vie saine). Elle permet de :

- **Gérer des données alimentaires** de 13 pays africains
- **Détecter les allergies alimentaires** via des algorithmes probabilistes
- **Planifier des repas hebdomadaires** personnalisés
- **Organiser des buffets de cérémonie** avec gestion budgétaire
- **Analyser les risques allergiques** basés sur l'historique de consommation

## ✨ Fonctionnalités

### 🔐 Gestion des Entités de Base
- **Personnes** : Création, modification, suppression de profils utilisateur
- **Aliments** : Base de données d'aliments africains avec descriptions
- **Ingrédients** : Gestion détaillée des composants alimentaires
- **Allergies** : Suivi des allergies par personne et ingrédient

### 🧠 Intelligence Alimentaire
- **Détection d'Allergènes** : Vérification automatique des risques
- **Analyse Probabiliste** : Calcul des probabilités d'allergie
- **Historique de Consommation** : Suivi des réactions alimentaires
- **Recommandations** : Suggestions basées sur l'historique

### 📅 Planification
- **Plans de Repas Hebdomadaires** : Organisation sur 7 jours
- **Listes de Courses** : Génération automatique
- **Gestion de Buffets** : Organisation d'événements avec budget
- **Analyse Budgétaire** : Suivi des coûts

## 🛠️ Technologies Utilisées

| Composant | Technologie | Version |
|-----------|-------------|---------|
| **Backend** | Flask | Latest |
| **Base de Données** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | Latest |
| **Langage** | Python | 3.10+ |
| **Containerisation** | Docker & Docker Compose | Latest |
| **Cache** | Redis | 7 |
| **Proxy** | Nginx | Alpine |
| **Admin BDD** | pgAdmin | Latest |

## 🚀 Installation et Démarrage

### Prérequis
- Docker et Docker Compose installés
- Git installé
- Port 5000, 80, 5433, 6379, 8080 disponibles

### 1. Cloner le Projet
```bash
git clone https://github.com/thesilentghost777/Food_managment.git
cd food-management-app
```

### 2. Démarrer l'Application
```bash
# Démarrage complet de tous les services
docker-compose up -d

# Pour voir les logs en temps réel
docker-compose up

# Arrêter l'application
docker-compose down

# Reconstruction complète (après modification)
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 3. Vérifier le Démarrage
```bash
# Vérifier l'état des conteneurs
docker-compose ps

# Voir les logs d'un service spécifique
docker-compose logs web
docker-compose logs postgres
```

### 4. Accès aux Services

| Service | URL | Identifiants |
|---------|-----|--------------|
| **API Principal** | http://localhost:5000 | - |
| **Interface Web** | http://localhost:80 | - |
| **pgAdmin** | http://localhost:8080 | admin@foodmanagement.com / admin123 |
| **PostgreSQL** | localhost:5433 | ghost / ghost |
| **Redis** | localhost:6379 | - |

## 📡 API Endpoints

### 👤 Gestion des Personnes
```http
GET    /api/persons/              # Liste toutes les personnes
POST   /api/persons/              # Crée une nouvelle personne
GET    /api/persons/{id}          # Récupère une personne spécifique
PUT    /api/persons/{id}          # Met à jour une personne
DELETE /api/persons/{id}          # Supprime une personne
GET    /api/persons/{id}/allergies # Allergies d'une personne
```

### 🍽️ Gestion des Aliments
```http
GET    /api/foods/                    # Liste tous les aliments
POST   /api/foods/                    # Crée un nouvel aliment
GET    /api/foods/{id}                # Récupère un aliment spécifique
PUT    /api/foods/{id}                # Met à jour un aliment
DELETE /api/foods/{id}                # Supprime un aliment
GET    /api/foods/{id}/ingredients    # Ingrédients d'un aliment
```

### 🥕 Gestion des Ingrédients
```http
GET    /api/ingredients/         # Liste tous les ingrédients
POST   /api/ingredients/         # Crée un nouvel ingrédient
GET    /api/ingredients/{id}     # Récupère un ingrédient spécifique
PUT    /api/ingredients/{id}     # Met à jour un ingrédient
DELETE /api/ingredients/{id}     # Supprime un ingrédient
```

### 🚨 Gestion des Allergies
```http
GET    /api/allergies/           # Liste toutes les allergies
POST   /api/allergies/           # Déclare une nouvelle allergie
GET    /api/allergies/{id}       # Récupère une allergie spécifique
DELETE /api/allergies/{id}       # Supprime une allergie
```

### 📊 Consommation et Analyses
```http
POST   /api/consumptions/declare                    # Déclare une consommation
GET    /api/consumptions/view/{person_id}           # Historique de consommation
PUT    /api/consumptions/update/{id}                # Met à jour une consommation
DELETE /api/consumptions/delete/{id}                # Supprime une consommation
POST   /api/consumptions/allergy/check              # Vérifie les allergies
POST   /api/consumptions/allergy/detailed-check     # Analyse détaillée
```

### 📅 Planification de Repas
```http
POST   /api/meal-planning/                                    # Crée un plan de repas
GET    /api/meal-planning/person/{person_id}/week/{date}      # Plan hebdomadaire
PUT    /api/meal-planning/{id}                                # Modifie un plan
DELETE /api/meal-planning/{id}                                # Supprime un plan
GET    /api/meal-planning/person/{person_id}/shopping-list/{date} # Liste de courses
POST   /api/meal-planning/person/{person_id}/mark-prepared    # Marque comme préparé
```

### 🎉 Gestion de Buffets
```http
GET    /api/ceremony-buffet/                    # Liste tous les buffets
POST   /api/ceremony-buffet/                    # Crée un nouveau buffet
GET    /api/ceremony-buffet/{id}                # Détails d'un buffet
PUT    /api/ceremony-buffet/{id}                # Modifie un buffet
DELETE /api/ceremony-buffet/{id}                # Supprime un buffet
GET    /api/ceremony-buffet/organizer/{id}      # Buffets d'un organisateur
GET    /api/ceremony-buffet/budget-analysis     # Analyse budgétaire
POST   /api/ceremony-buffet/{id}/confirm        # Confirme un buffet
```

## 🧪 Tests avec Postman

### Import de la Collection
1. Ouvrir Postman
2. Importer le fichier `postman_collection.json`
3. Configurer la variable `base_url` : `http://localhost:5000`

### Scénarios de Test Principaux

#### 🎯 Scénario 1 : Configuration de Base
```bash
# 1. Créer une personne
POST /api/persons/
{
  "name": "Signe Fongang",
  "age": 18,
  "sexe": "male"
}

# 2. Créer un aliment
POST /api/foods/
{
  "name": "Thieboudienne", 
  "description": "Plat national du Sénégal à base de riz et poisson"
}

# 3. Ajouter des ingrédients
POST /api/ingredients/
{
  "food_id": 1, 
  "name": "Poisson", 
  "description": "Poisson frais", 
  "is_allergen": true
}
```

#### 🧠 Scénario 2 : Test des Allergies
```bash
# 1. Déclarer une consommation avec problème
POST /api/consumptions/declare
{
  "person_id": 1,
  "food_id": 1,
  "had_problem": true,
  "problem_details": "Réaction allergique légère",
  "severity_level": "mild",
  "symptoms": "Rougeurs, démangeaisons"
}

# 2. Vérifier les probabilités d'allergie
POST /api/consumptions/allergy/check
{
  "person_id": 1,
  "food_id": 1
}
```

#### 📅 Scénario 3 : Planification Hebdomadaire
```bash
# 1. Créer un plan de repas
POST /api/meal-planning/
{
  "person_id": 1,
  "week_start_date": "2025-06-09",
  "day_of_week": 1,
  "meal_type": "lunch",
  "food_id": 1,
  "quantity": 2
}

# 2. Récupérer la planification
GET /api/meal-planning/person/1/week/2025-06-09

# 3. Générer liste de courses
GET /api/meal-planning/person/1/shopping-list/2025-06-09
```

#### 🎉 Scénario 4 : Gestion de Buffet
```bash
# 1. Créer un buffet de cérémonie
POST /api/ceremony-buffet/
{
  "ceremony_name": "Mariage de Paul et Marie",
  "ceremony_date": "2025-07-15 18:00:00",
  "organizer_person_id": 1,
  "expected_guests": 150,
  "location": "Salle des fêtes Yaoundé",
  "budget": 500000,
  "food_id": 1,
  "quantity_needed": 10,
  "cost_per_unit": 15000
}

# 2. Analyser les coûts
GET /api/ceremony-buffet/budget-analysis

# 3. Confirmer le buffet
POST /api/ceremony-buffet/1/confirm
```

### Headers Requis
```http
Content-Type: application/json
Accept: application/json
```

### Codes de Réponse
- **200** : Succès
- **201** : Création réussie
- **400** : Erreur de validation
- **404** : Ressource non trouvée
- **500** : Erreur serveur

## 📁 Structure du Projet

```
food-management-app/
├── 📁 app/
│   ├── 📄 __init__.py          # Configuration Flask
│   ├── 📄 models.py            # Modèles SQLAlchemy
│   ├── 📄 routes/              # Routes organisées par module
│   │   ├── 📄 persons.py
│   │   ├── 📄 foods.py
│   │   ├── 📄 ingredients.py
│   │   ├── 📄 allergies.py
│   │   ├── 📄 consumptions.py
│   │   ├── 📄 meal_planning.py
│   │   └── 📄 ceremony_buffet.py
│   └── 📄 utils.py             # Fonctions utilitaires
├── 📄 docker-compose.yml       # Configuration Docker Compose
├── 📄 Dockerfile              # Image Docker de l'app
├── 📄 requirements_docker.txt  # Dépendances Python
├── 📄 wsgi.py                 # Point d'entrée WSGI
├── 📄 postman_collection.json # Collection Postman
├── 📁 nginx/                  # Configuration Nginx
├── 📁 instance/               # Fichiers d'instance
├── 📁 logs/                   # Logs de l'application
└── 📄 README.md               # Ce fichier
```

## 🌍 Pays Couverts

L'application couvre les cuisines de **13 pays africains** :

| Région | Pays |
|--------|------|
| **Afrique du Nord** | Algérie, Égypte, Maroc, Tunisie |
| **Afrique de l'Ouest** | Côte d'Ivoire, Nigeria, Guinée Équatoriale |
| **Afrique Centrale** | Cameroun, RDC |
| **Afrique de l'Est** | Kenya, Tanzanie, Somalie |
| **Afrique Australe** | Afrique du Sud |

## 🐛 Dépannage

### Problèmes Courants

#### Port déjà utilisé
```bash
# Vérifier les ports occupés
netstat -tulpn | grep :5000
# Ou utiliser un autre port
sed -i 's/5000:5000/5001:5000/g' docker-compose.yml
```

#### Erreur de connexion base de données
```bash
# Redémarrer PostgreSQL
docker-compose restart postgres
# Vérifier les logs
docker-compose logs postgres
```

#### Problème de permissions
```bash
# Corriger les permissions
sudo chown -R $USER:$USER .
chmod -R 755 .
```

### Logs et Monitoring
```bash
# Logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f web
docker-compose logs -f postgres

# État des conteneurs
docker-compose ps

# Utilisation des ressources
docker stats
```

## 🔧 Configuration Avancée

### Variables d'Environnement
Modifiez le fichier `docker-compose.yml` pour personnaliser :

```yaml
environment:
  - FLASK_ENV=production        # development pour debug
  - SECRET_KEY=votre-clé-secrète
  - DB_HOST=postgres
  - DB_PORT=5432
  - DB_NAME=food_management
  - DB_USER=ghost
  - DB_PASSWORD=ghost
```

### Personnalisation des Ports
```yaml
ports:
  - "8000:5000"  # API sur port 8000
  - "8080:80"    # Web sur port 8080
  - "5434:5432"  # PostgreSQL sur port 5434
```

## 📈 Performances et Monitoring

### Métriques Disponibles
- **Temps de réponse API** : Via logs Nginx
- **Utilisation CPU/RAM** : `docker stats`
- **Requêtes BDD** : Via pgAdmin
- **Cache Redis** : Connexion directe sur port 6379

### Optimisations
- **Cache Redis** : Mise en cache des requêtes fréquentes
- **Index BDD** : Index optimisés sur les clés étrangères
- **Workers Gunicorn** : 2 workers par défaut (ajustable)
- **Timeout** : 120s pour les requêtes longues

## 🤝 Contribution

### Développement Local
```bash
# Cloner le projet
git clone https://github.com/thesilentghost777/Food_managment.git
cd food-management-app

# Développement sans Docker
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements_docker.txt

# Variables d'environnement
cp .env.example .env
# Modifier les variables dans .env

# Lancer en mode développement
flask run --debug --host=0.0.0.0 --port=5000
```

### Structure des Commits
```
feat: nouvelle fonctionnalité
fix: correction de bug
docs: documentation
refactor: refactorisation
test: ajout de tests
```

## 📞 Support

### Informations Développeur
- **Développeur** : SIGNE FONGANG WILFRIED BRANDON
- **Matricule** : 23U2833
- **Université** : Université de Yaoundé I
- **Cours** : INF222 - Développement Web

### Issues et Bugs
Pour signaler un problème ou demander une fonctionnalité :
1. Vérifiez les issues existantes
2. Créez une nouvelle issue avec :
   - Description claire du problème
   - Étapes de reproduction
   - Logs d'erreur si applicable
   - Configuration système

## 📄 Licence

Ce projet est développé dans le cadre académique à l'Université de Yaoundé I.

---

**🎯 Objectif** : Contribuer aux ODD 2 (Faim Zéro) et ODD 3 (Vie Saine) à travers une gestion intelligente de l'alimentation.

**🚀 Status** : Production Ready - Dockerisé et optimisé pour le déploiement.

**📅 Dernière Mise à Jour** : Juin 2025
