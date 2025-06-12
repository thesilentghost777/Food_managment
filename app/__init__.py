import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Créer l'instance SQLAlchemy ici
db = SQLAlchemy()


def init_database():
    from app import db
    from app.models import Food, Ingredient

    # Vérifier si les tables existent avant de les supprimer
    try:
        # Créer les tables d'abord si elles n'existent pas
        db.create_all()
        
        # Vérifier s'il y a déjà des données dans la table Food
        existing_foods = Food.query.first()
        if existing_foods:
            print("✔ Base de données déjà initialisée.")
            return
            
    except Exception as e:
        print(f"Erreur lors de la vérification des tables: {e}")
        # Si erreur, on continue avec la création des tables
        db.create_all()

    plats = []

    # 1. Ndolé
    ndole = Food(
        name="Ndolé",
        description="Plat traditionnel camerounais à base de feuilles de ndolé et d'arachides"
    )
    plats.append((ndole, [
        Ingredient(name="Feuilles de ndolé"),
        Ingredient(name="Arachides", is_allergen=True),
        Ingredient(name="Viande de bœuf"),
        Ingredient(name="Poisson fumé", is_allergen=True),
        Ingredient(name="Crevettes", is_allergen=True)
    ]))

    # 2. Eru
    eru = Food(
        name="Eru",
        description="Soupe traditionnelle à base de feuilles d'eru et de coco râpé"
    )
    plats.append((eru, [
        Ingredient(name="Feuilles d'eru"),
        Ingredient(name="Coco râpé"),
        Ingredient(name="Viande de chèvre"),
        Ingredient(name="Poisson sec", is_allergen=True),
        Ingredient(name="Huile de palme")
    ]))

    # 3. Poulet DG
    poulet_dg = Food(
        name="Poulet DG",
        description="Poulet sauté aux légumes et plantains, plat moderne camerounais"
    )
    plats.append((poulet_dg, [
        Ingredient(name="Poulet"),
        Ingredient(name="Plantains"),
        Ingredient(name="Carottes"),
        Ingredient(name="Haricots verts"),
        Ingredient(name="Ail")
    ]))

    # 4. Koki
    koki = Food(
        name="Koki",
        description="Gâteau de haricots cuit à la vapeur dans des feuilles"
    )
    plats.append((koki, [
        Ingredient(name="Haricots noirs"),
        Ingredient(name="Huile de palme"),
        Ingredient(name="Gingembre"),
        Ingredient(name="Piment"),
        Ingredient(name="Feuilles de bananier")
    ]))

    # 5. Achu
    achu = Food(
        name="Achu",
        description="Plat traditionnel à base de taro pilé et sauce jaune"
    )
    plats.append((achu, [
        Ingredient(name="Taro"),
        Ingredient(name="Huile de palme"),
        Ingredient(name="Épices kankankan"),
        Ingredient(name="Viande de bœuf"),
        Ingredient(name="Poisson fumé", is_allergen=True)
    ]))

    try:
        for food, ingredients in plats:
            db.session.add(food)
            db.session.flush()  # pour avoir food.id
            for ing in ingredients:
                ing.food_id = food.id
                db.session.add(ing)

        db.session.commit()
        print("✔ Base de données initialisée avec les plats traditionnels.")
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors de l'initialisation: {e}")

    
def create_app():
    # Charger les variables d'environnement à partir du fichier .env
    load_dotenv()
    app = Flask(__name__)
    
    # Configuration de l'app Flask avec les variables d'environnement
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'changeme')
    
    # Initialiser SQLAlchemy avec l'app
    db.init_app(app)
    
    # Importer les modèles APRÈS l'initialisation de db
    from . import models
    
    # Importer et enregistrer les blueprints (routes) APRÈS l'importation des modèles
    from .routes.person_routes import person_bp
    from .routes.food_routes import food_bp
    from .routes.allergy_routes import allergy_bp
    from .routes.ingredient_routes import ingredient_bp
    from .routes.consumption_routes import consumption_bp  # Nouvelle route ajoutée
    from .routes.meal_planning_routes import meal_planning_bp
    from .routes.ceremony_buffet_routes import ceremony_buffet_bp
    
    app.register_blueprint(person_bp, url_prefix="/api/persons")
    app.register_blueprint(food_bp, url_prefix="/api/foods")
    app.register_blueprint(allergy_bp, url_prefix="/api/allergies")
    app.register_blueprint(ingredient_bp, url_prefix="/api/ingredients")
    app.register_blueprint(consumption_bp, url_prefix="/api/consumptions")  # Enregistrement du nouveau blueprint
     # Enregistrer les nouveaux blueprints
    app.register_blueprint(meal_planning_bp, url_prefix="/api/meal-planning")
    app.register_blueprint(ceremony_buffet_bp, url_prefix="/api/ceremony-buffet")
    
    # Créer les tables si elles n'existent pas encore
    with app.app_context():
        db.create_all()
        init_database()
    
    return app
