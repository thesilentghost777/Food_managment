from flask import Blueprint, request, jsonify
from app import db
from app.models import WeeklyMealPlan, Person, Food, Ingredient, Allergy
from datetime import datetime, date, timedelta
from sqlalchemy import and_

meal_planning_bp = Blueprint('meal_planning', __name__)

@meal_planning_bp.route('/', methods=['POST'])
def create_meal_plan():
    """Ajouter un repas à la planification hebdomadaire"""
    try:
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['person_id', 'week_start_date', 'day_of_week', 'meal_type', 'food_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        # Vérification que la personne existe
        person = Person.query.get(data['person_id'])
        if not person:
            return jsonify({'error': 'Personne non trouvée'}), 404
            
        # Vérification que la nourriture existe
        food = Food.query.get(data['food_id'])
        if not food:
            return jsonify({'error': 'Nourriture non trouvée'}), 404
        
        # Vérification des allergies
        person_allergies = [allergy.ingredient_id for allergy in person.allergies]
        food_allergens = [ing.id for ing in food.ingredients if ing.is_allergen]
        
        conflicting_allergens = set(person_allergies) & set(food_allergens)
        if conflicting_allergens:
            allergen_names = [Ingredient.query.get(aid).name for aid in conflicting_allergens]
            return jsonify({
                'warning': f'Attention: Ce plat contient des allergènes pour cette personne: {", ".join(allergen_names)}',
                'allergens': allergen_names
            }), 200
        
        # Conversion de la date
        week_start_date = datetime.strptime(data['week_start_date'], '%Y-%m-%d').date()
        
        meal_plan = WeeklyMealPlan(
            person_id=data['person_id'],
            week_start_date=week_start_date,
            day_of_week=data['day_of_week'],
            meal_type=data['meal_type'],
            food_id=data['food_id'],
            quantity=data.get('quantity', 1),
            notes=data.get('notes', '')
        )
        
        db.session.add(meal_plan)
        db.session.commit()
        
        return jsonify({
            'id': meal_plan.id,
            'person_name': person.name,
            'food_name': food.name,
            'week_start_date': meal_plan.week_start_date.isoformat(),
            'day_of_week': meal_plan.day_of_week,
            'meal_type': meal_plan.meal_type,
            'quantity': meal_plan.quantity,
            'notes': meal_plan.notes,
            'is_prepared': meal_plan.is_prepared
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@meal_planning_bp.route('/person/<int:person_id>/week/<string:week_start>', methods=['GET'])
def get_weekly_plan(person_id, week_start):
    """Récupérer la planification d'une semaine pour une personne"""
    try:
        week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
        
        meal_plans = WeeklyMealPlan.query.filter(
            and_(
                WeeklyMealPlan.person_id == person_id,
                WeeklyMealPlan.week_start_date == week_start_date
            )
        ).join(Food).all()
        
        # Organisation par jour et type de repas
        weekly_plan = {}
        days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
        
        for i in range(1, 8):
            day_name = days[i-1]
            weekly_plan[day_name] = {
                'breakfast': [],
                'lunch': [],
                'dinner': [],
                'snack': []
            }
        
        for plan in meal_plans:
            day_name = days[plan.day_of_week - 1]
            weekly_plan[day_name][plan.meal_type].append({
                'id': plan.id,
                'food_name': plan.food.name,
                'food_description': plan.food.description,
                'quantity': plan.quantity,
                'notes': plan.notes,
                'is_prepared': plan.is_prepared
            })
        
        return jsonify({
            'person_id': person_id,
            'week_start_date': week_start,
            'weekly_plan': weekly_plan
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@meal_planning_bp.route('/<int:plan_id>', methods=['PUT'])
def update_meal_plan(plan_id):
    """Modifier un élément de la planification"""
    try:
        meal_plan = WeeklyMealPlan.query.get(plan_id)
        if not meal_plan:
            return jsonify({'error': 'Plan de repas non trouvé'}), 404
        
        data = request.get_json()
        
        # Mise à jour des champs modifiables
        if 'quantity' in data:
            meal_plan.quantity = data['quantity']
        if 'notes' in data:
            meal_plan.notes = data['notes']
        if 'is_prepared' in data:
            meal_plan.is_prepared = data['is_prepared']
        if 'food_id' in data:
            food = Food.query.get(data['food_id'])
            if food:
                meal_plan.food_id = data['food_id']
            else:
                return jsonify({'error': 'Nourriture non trouvée'}), 404
        
        db.session.commit()
        
        return jsonify({
            'id': meal_plan.id,
            'food_name': meal_plan.food.name,
            'quantity': meal_plan.quantity,
            'notes': meal_plan.notes,
            'is_prepared': meal_plan.is_prepared,
            'message': 'Plan de repas mis à jour avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@meal_planning_bp.route('/<int:plan_id>', methods=['DELETE'])
def delete_meal_plan(plan_id):
    """Supprimer un élément de la planification"""
    try:
        meal_plan = WeeklyMealPlan.query.get(plan_id)
        if not meal_plan:
            return jsonify({'error': 'Plan de repas non trouvé'}), 404
        
        db.session.delete(meal_plan)
        db.session.commit()
        
        return jsonify({'message': 'Plan de repas supprimé avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@meal_planning_bp.route('/person/<int:person_id>/shopping-list/<string:week_start>', methods=['GET'])
def generate_shopping_list(person_id, week_start):
    """Générer une liste de courses pour la semaine"""
    try:
        week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
        
        meal_plans = WeeklyMealPlan.query.filter(
            and_(
                WeeklyMealPlan.person_id == person_id,
                WeeklyMealPlan.week_start_date == week_start_date,
                WeeklyMealPlan.is_prepared == False
            )
        ).join(Food).join(Ingredient).all()
        
        # Regrouper les ingrédients
        ingredients_needed = {}
        for plan in meal_plans:
            for ingredient in plan.food.ingredients:
                if ingredient.name not in ingredients_needed:
                    ingredients_needed[ingredient.name] = {
                        'total_quantity': 0,
                        'is_allergen': ingredient.is_allergen,
                        'used_in_foods': []
                    }
                ingredients_needed[ingredient.name]['total_quantity'] += plan.quantity
                if plan.food.name not in ingredients_needed[ingredient.name]['used_in_foods']:
                    ingredients_needed[ingredient.name]['used_in_foods'].append(plan.food.name)
        
        return jsonify({
            'person_id': person_id,
            'week_start_date': week_start,
            'shopping_list': ingredients_needed
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@meal_planning_bp.route('/person/<int:person_id>/mark-prepared', methods=['POST'])
def mark_meals_prepared(person_id):
    """Marquer des repas comme préparés"""
    try:
        data = request.get_json()
        meal_plan_ids = data.get('meal_plan_ids', [])
        
        if not meal_plan_ids:
            return jsonify({'error': 'Aucun ID de plan de repas fourni'}), 400
        
        updated_count = WeeklyMealPlan.query.filter(
            and_(
                WeeklyMealPlan.id.in_(meal_plan_ids),
                WeeklyMealPlan.person_id == person_id
            )
        ).update({'is_prepared': True})
        
        db.session.commit()
        
        return jsonify({
            'message': f'{updated_count} repas marqués comme préparés',
            'updated_count': updated_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
