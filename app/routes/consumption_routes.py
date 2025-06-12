from flask import Blueprint, request, jsonify
from app import db
from app.models import Person, Food, Ingredient, Consumption, Allergy
from datetime import datetime
from sqlalchemy import and_

consumption_bp = Blueprint('consumption', __name__)

@consumption_bp.route('/declare', methods=['POST'])
def declare_consumption():
    """API pour déclarer une nouvelle consommation"""
    try:
        # Récupération des données JSON
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        # Validation des données obligatoires
        person_id = data.get('person_id')
        food_id = data.get('food_id')
        
        if not person_id or not food_id:
            return jsonify({'error': 'person_id et food_id sont obligatoires'}), 400
        
        # Vérification de l'existence de la personne et de la nourriture
        person = Person.query.get(person_id)
        food = Food.query.get(food_id)
        
        if not person:
            return jsonify({'error': f'Personne avec ID {person_id} non trouvée'}), 404
        
        if not food:
            return jsonify({'error': f'Nourriture avec ID {food_id} non trouvée'}), 404
        
        # Récupération des autres données
        had_problem = data.get('had_problem', False)
        problem_details = data.get('problem_details', '')
        severity_level = data.get('severity_level', '')
        symptoms = data.get('symptoms', '')
        notes = data.get('notes', '')
        consumption_date_str = data.get('consumption_date')
        
        # Conversion de la date
        consumption_date = datetime.utcnow()
        if consumption_date_str:
            try:
                consumption_date = datetime.fromisoformat(consumption_date_str.replace('Z', '+00:00'))
            except ValueError:
                try:
                    consumption_date = datetime.strptime(consumption_date_str, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    return jsonify({'error': 'Format de date invalide. Utilisez ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        
        # Création de la consommation
        consumption = Consumption(
            person_id=int(person_id),
            food_id=int(food_id),
            consumption_date=consumption_date,
            had_problem=had_problem,
            problem_details=problem_details if had_problem else None,
            severity_level=severity_level if had_problem and severity_level else None,
            symptoms=symptoms if had_problem else None,
            notes=notes if notes else None
        )
        
        db.session.add(consumption)
        db.session.commit()
        
        return jsonify({
            'message': 'Consommation déclarée avec succès',
            'consumption_id': consumption.id,
            'person_name': person.name,
            'food_name': food.name,
            'consumption_date': consumption.consumption_date.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la déclaration: {str(e)}'}), 500

@consumption_bp.route('/view/<int:person_id>', methods=['GET'])
def view_consumptions(person_id):
    """API pour consulter les consommations d'une personne"""
    try:
        person = Person.query.get(person_id)
        if not person:
            return jsonify({'error': f'Personne avec ID {person_id} non trouvée'}), 404
        
        consumptions = Consumption.query.filter_by(person_id=person_id).order_by(
            Consumption.consumption_date.desc()
        ).all()
        
        # Statistiques
        total_consumptions = len(consumptions)
        problem_consumptions = len([c for c in consumptions if c.had_problem])
        problem_rate = (problem_consumptions / total_consumptions * 100) if total_consumptions > 0 else 0
        
        # Formatage des données
        consumptions_data = []
        for c in consumptions:
            consumptions_data.append({
                'id': c.id,
                'food_id': c.food_id,
                'food_name': c.food.name,
                'consumption_date': c.consumption_date.isoformat(),
                'had_problem': c.had_problem,
                'problem_details': c.problem_details,
                'severity_level': c.severity_level,
                'symptoms': c.symptoms,
                'notes': c.notes
            })
        
        return jsonify({
            'person': {
                'id': person.id,
                'name': person.name
            },
            'statistics': {
                'total_consumptions': total_consumptions,
                'problem_consumptions': problem_consumptions,
                'problem_rate': round(problem_rate, 2)
            },
            'consumptions': consumptions_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la récupération des consommations: {str(e)}'}), 500

@consumption_bp.route('/allergy/check', methods=['POST'])
def check_allergy_probability():
    """API pour vérifier la probabilité d'allergie à une nourriture"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        person_id = data.get('person_id')
        food_id = data.get('food_id')
        
        if not person_id or not food_id:
            return jsonify({'error': 'person_id et food_id sont obligatoires'}), 400
        
        person = Person.query.get(person_id)
        food = Food.query.get(food_id)
        
        if not person:
            return jsonify({'error': f'Personne avec ID {person_id} non trouvée'}), 404
        
        if not food:
            return jsonify({'error': f'Nourriture avec ID {food_id} non trouvée'}), 404
        
        # Calcul de la probabilité d'allergie
        probability = calculate_allergy_probability(person_id, food_id)
        is_allergic = probability > 0.3
        
        return jsonify({
            'person': {
                'id': person.id,
                'name': person.name
            },
            'food': {
                'id': food.id,
                'name': food.name
            },
            'allergy_analysis': {
                'probability': round(probability, 3),
                'is_allergic': is_allergic,
                'risk_level': get_risk_level(probability)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consumption_bp.route('/allergy/detailed-check', methods=['POST'])
def check_allergy_detailed():
    """API pour vérification d'allergie avec détails des consommations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        person_id = data.get('person_id')
        food_id = data.get('food_id')
        
        if not person_id or not food_id:
            return jsonify({'error': 'person_id et food_id sont obligatoires'}), 400
        
        person = Person.query.get(person_id)
        food = Food.query.get(food_id)
        
        if not person:
            return jsonify({'error': f'Personne avec ID {person_id} non trouvée'}), 404
        
        if not food:
            return jsonify({'error': f'Nourriture avec ID {food_id} non trouvée'}), 404
        
        # Calcul de la probabilité
        probability = calculate_allergy_probability(person_id, food_id)
        is_allergic = probability > 0.3
        
        # Récupération des consommations liées
        consumptions = Consumption.query.filter_by(
            person_id=person_id, 
            food_id=food_id
        ).order_by(Consumption.consumption_date.desc()).all()
        
        consumptions_data = []
        for c in consumptions:
            consumptions_data.append({
                'id': c.id,
                'consumption_date': c.consumption_date.isoformat(),
                'had_problem': c.had_problem,
                'problem_details': c.problem_details,
                'severity_level': c.severity_level,
                'symptoms': c.symptoms,
                'notes': c.notes
            })
        
        return jsonify({
            'person': {
                'id': person.id,
                'name': person.name
            },
            'food': {
                'id': food.id,
                'name': food.name
            },
            'allergy_analysis': {
                'probability': round(probability, 3),
                'is_allergic': is_allergic,
                'risk_level': get_risk_level(probability)
            },
            'consumption_history': consumptions_data,
            'statistics': {
                'total_consumptions': len(consumptions_data),
                'problem_consumptions': len([c for c in consumptions_data if c['had_problem']])
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la vérification: {str(e)}'}), 500

@consumption_bp.route('/update/<int:consumption_id>', methods=['PUT'])
def update_consumption(consumption_id):
    """API pour mettre à jour une consommation existante"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        consumption = Consumption.query.get(consumption_id)
        if not consumption:
            return jsonify({'error': f'Consommation avec ID {consumption_id} non trouvée'}), 404
        
        # Mise à jour des champs modifiables
        if 'had_problem' in data:
            consumption.had_problem = data['had_problem']
        
        if 'problem_details' in data:
            consumption.problem_details = data['problem_details'] if consumption.had_problem else None
        
        if 'severity_level' in data:
            consumption.severity_level = data['severity_level'] if consumption.had_problem else None
        
        if 'symptoms' in data:
            consumption.symptoms = data['symptoms'] if consumption.had_problem else None
        
        if 'notes' in data:
            consumption.notes = data['notes']
        
        if 'consumption_date' in data:
            try:
                consumption.consumption_date = datetime.fromisoformat(data['consumption_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Format de date invalide'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Consommation mise à jour avec succès',
            'consumption': {
                'id': consumption.id,
                'person_id': consumption.person_id,
                'food_id': consumption.food_id,
                'consumption_date': consumption.consumption_date.isoformat(),
                'had_problem': consumption.had_problem,
                'problem_details': consumption.problem_details,
                'severity_level': consumption.severity_level,
                'symptoms': consumption.symptoms,
                'notes': consumption.notes
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la mise à jour: {str(e)}'}), 500

@consumption_bp.route('/delete/<int:consumption_id>', methods=['DELETE'])
def delete_consumption(consumption_id):
    """API pour supprimer une consommation"""
    try:
        consumption = Consumption.query.get(consumption_id)
        if not consumption:
            return jsonify({'error': f'Consommation avec ID {consumption_id} non trouvée'}), 404
        
        db.session.delete(consumption)
        db.session.commit()
        
        return jsonify({
            'message': f'Consommation {consumption_id} supprimée avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erreur lors de la suppression: {str(e)}'}), 500

@consumption_bp.route('/persons', methods=['GET'])
def get_all_persons():
    """API pour récupérer toutes les personnes"""
    try:
        persons = Person.query.all()
        persons_data = [{'id': p.id, 'name': p.name} for p in persons]
        
        return jsonify({
            'persons': persons_data,
            'count': len(persons_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consumption_bp.route('/api/foods', methods=['GET'])
def get_all_foods():
    """API pour récupérer toutes les nourritures"""
    try:
        foods = Food.query.all()
        foods_data = []
        
        for f in foods:
            food_data = {
                'id': f.id,
                'name': f.name
            }
            # Ajouter les ingrédients si disponibles
            if hasattr(f, 'ingredients') and f.ingredients:
                food_data['ingredients'] = [{'id': ing.id, 'name': ing.name} for ing in f.ingredients]
            
            foods_data.append(food_data)
        
        return jsonify({
            'foods': foods_data,
            'count': len(foods_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_allergy_probability(person_id, food_id):
    """Calcule la probabilité d'allergie basée sur l'historique de consommation"""
    # Récupération de toutes les consommations de cette nourriture par cette personne
    consumptions = Consumption.query.filter_by(
        person_id=person_id, 
        food_id=food_id
    ).all()
    
    if not consumptions:
        return 0.0
    
    # Calcul de base: ratio de problèmes
    total_consumptions = len(consumptions)
    problem_consumptions = len([c for c in consumptions if c.had_problem])
    base_probability = problem_consumptions / total_consumptions
    
    # Facteurs d'ajustement
    severity_weight = 0
    for consumption in consumptions:
        if consumption.had_problem and consumption.severity_level:
            if consumption.severity_level == 'severe':
                severity_weight += 0.3
            elif consumption.severity_level == 'moderate':
                severity_weight += 0.2
            elif consumption.severity_level == 'mild':
                severity_weight += 0.1
    
    # Vérification des allergies connues aux ingrédients
    ingredient_allergy_factor = 0
    food = Food.query.get(food_id)
    if food and hasattr(food, 'ingredients') and food.ingredients:
        known_allergies = Allergy.query.filter_by(person_id=person_id).all()
        allergic_ingredient_ids = [allergy.ingredient_id for allergy in known_allergies]
        
        food_ingredient_ids = [ingredient.id for ingredient in food.ingredients]
        common_allergens = set(allergic_ingredient_ids) & set(food_ingredient_ids)
        
        if common_allergens:
            ingredient_allergy_factor = 0.4
    
    # Calcul final
    final_probability = min(1.0, base_probability + (severity_weight / total_consumptions) + ingredient_allergy_factor)
    
    return final_probability

def get_risk_level(probability):
    """Détermine le niveau de risque basé sur la probabilité"""
    if probability > 0.7:
        return 'Très élevé'
    elif probability > 0.5:
        return 'Élevé'
    elif probability > 0.3:
        return 'Modéré'
    elif probability > 0.1:
        return 'Faible'
    else:
        return 'Très faible'
