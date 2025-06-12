from flask import Blueprint, request, jsonify
from app import db
from app.models import CeremonyBuffet, Person, Food, Ingredient, Allergy
from datetime import datetime
from sqlalchemy import and_, func

ceremony_buffet_bp = Blueprint('ceremony_buffet', __name__)

@ceremony_buffet_bp.route('/', methods=['POST'])
def create_ceremony_buffet():
    """Créer un nouveau buffet de cérémonie"""
    try:
        data = request.get_json()
        
        # Validation des données requises
        required_fields = ['ceremony_name', 'ceremony_date', 'organizer_person_id', 'expected_guests', 'food_id', 'quantity_needed']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Le champ {field} est requis'}), 400
        
        # Vérifications d'existence
        organizer = Person.query.get(data['organizer_person_id'])
        if not organizer:
            return jsonify({'error': 'Organisateur non trouvé'}), 404
            
        food = Food.query.get(data['food_id'])
        if not food:
            return jsonify({'error': 'Nourriture non trouvée'}), 404
        
        # Conversion de la date
        ceremony_date = datetime.strptime(data['ceremony_date'], '%Y-%m-%d %H:%M:%S')
        
        buffet = CeremonyBuffet(
            ceremony_name=data['ceremony_name'],
            ceremony_date=ceremony_date,
            organizer_person_id=data['organizer_person_id'],
            expected_guests=data['expected_guests'],
            location=data.get('location', ''),
            budget=data.get('budget'),
            food_id=data['food_id'],
            quantity_needed=data['quantity_needed'],
            cost_per_unit=data.get('cost_per_unit'),
            special_requirements=data.get('special_requirements', ''),
            supplier_info=data.get('supplier_info', ''),
            notes=data.get('notes', '')
        )
        
        db.session.add(buffet)
        db.session.commit()
        
        # Calcul du coût total
        total_cost = buffet.cost_per_unit * buffet.quantity_needed if buffet.cost_per_unit else None
        
        return jsonify({
            'id': buffet.id,
            'ceremony_name': buffet.ceremony_name,
            'ceremony_date': buffet.ceremony_date.isoformat(),
            'organizer_name': organizer.name,
            'expected_guests': buffet.expected_guests,
            'location': buffet.location,
            'budget': buffet.budget,
            'food_name': food.name,
            'quantity_needed': buffet.quantity_needed,
            'cost_per_unit': buffet.cost_per_unit,
            'total_cost': total_cost,
            'is_confirmed': buffet.is_confirmed,
            'special_requirements': buffet.special_requirements,
            'supplier_info': buffet.supplier_info,
            'notes': buffet.notes
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/', methods=['GET'])
def get_all_ceremonies():
    """Récupérer toutes les cérémonies"""
    try:
        ceremonies = CeremonyBuffet.query.join(Person).join(Food).all()
        
        result = []
        for ceremony in ceremonies:
            total_cost = ceremony.cost_per_unit * ceremony.quantity_needed if ceremony.cost_per_unit else None
            result.append({
                'id': ceremony.id,
                'ceremony_name': ceremony.ceremony_name,
                'ceremony_date': ceremony.ceremony_date.isoformat(),
                'organizer_name': ceremony.organizer.name,
                'expected_guests': ceremony.expected_guests,
                'location': ceremony.location,
                'budget': ceremony.budget,
                'food_name': ceremony.food.name,
                'quantity_needed': ceremony.quantity_needed,
                'total_cost': total_cost,
                'is_confirmed': ceremony.is_confirmed
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/<int:ceremony_id>', methods=['GET'])
def get_ceremony_details(ceremony_id):
    """Récupérer les détails d'une cérémonie avec analyse des allergènes"""
    try:
        ceremony = CeremonyBuffet.query.get(ceremony_id)
        if not ceremony:
            return jsonify({'error': 'Cérémonie non trouvée'}), 404
        
        # Analyse des allergènes potentiels
        food_allergens = [ing for ing in ceremony.food.ingredients if ing.is_allergen]
        allergen_info = []
        
        for allergen in food_allergens:
            # Compter combien de personnes pourraient être affectées
            affected_count = Allergy.query.filter_by(ingredient_id=allergen.id).count()
            allergen_info.append({
                'ingredient_name': allergen.name,
                'potentially_affected_guests': affected_count
            })
        
        total_cost = ceremony.cost_per_unit * ceremony.quantity_needed if ceremony.cost_per_unit else None
        cost_per_guest = total_cost / ceremony.expected_guests if total_cost and ceremony.expected_guests > 0 else None
        
        return jsonify({
            'id': ceremony.id,
            'ceremony_name': ceremony.ceremony_name,
            'ceremony_date': ceremony.ceremony_date.isoformat(),
            'organizer': {
                'id': ceremony.organizer_person_id,
                'name': ceremony.organizer.name,
                'age': ceremony.organizer.age,
                'sexe': ceremony.organizer.sexe
            },
            'expected_guests': ceremony.expected_guests,
            'location': ceremony.location,
            'budget': ceremony.budget,
            'food': {
                'id': ceremony.food_id,
                'name': ceremony.food.name,
                'description': ceremony.food.description,
                'ingredients': [{'name': ing.name, 'is_allergen': ing.is_allergen} for ing in ceremony.food.ingredients]
            },
            'quantity_needed': ceremony.quantity_needed,
            'cost_per_unit': ceremony.cost_per_unit,
            'total_cost': total_cost,
            'cost_per_guest': cost_per_guest,
            'is_confirmed': ceremony.is_confirmed,
            'special_requirements': ceremony.special_requirements,
            'supplier_info': ceremony.supplier_info,
            'notes': ceremony.notes,
            'allergen_analysis': allergen_info,
            'created_at': ceremony.created_at.isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/<int:ceremony_id>', methods=['PUT'])
def update_ceremony_buffet(ceremony_id):
    """Modifier un buffet de cérémonie"""
    try:
        ceremony = CeremonyBuffet.query.get(ceremony_id)
        if not ceremony:
            return jsonify({'error': 'Cérémonie non trouvée'}), 404
        
        data = request.get_json()
        
        # Mise à jour des champs modifiables
        updatable_fields = [
            'ceremony_name', 'expected_guests', 'location', 'budget',
            'quantity_needed', 'cost_per_unit', 'special_requirements',
            'supplier_info', 'notes', 'is_confirmed'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(ceremony, field, data[field])
        
        if 'ceremony_date' in data:
            ceremony.ceremony_date = datetime.strptime(data['ceremony_date'], '%Y-%m-%d %H:%M:%S')
        
        if 'food_id' in data:
            food = Food.query.get(data['food_id'])
            if food:
                ceremony.food_id = data['food_id']
            else:
                return jsonify({'error': 'Nourriture non trouvée'}), 404
        
        db.session.commit()
        
        total_cost = ceremony.cost_per_unit * ceremony.quantity_needed if ceremony.cost_per_unit else None
        
        return jsonify({
            'id': ceremony.id,
            'ceremony_name': ceremony.ceremony_name,
            'total_cost': total_cost,
            'is_confirmed': ceremony.is_confirmed,
            'message': 'Cérémonie mise à jour avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/<int:ceremony_id>', methods=['DELETE'])
def delete_ceremony_buffet(ceremony_id):
    """Supprimer un buffet de cérémonie"""
    try:
        ceremony = CeremonyBuffet.query.get(ceremony_id)
        if not ceremony:
            return jsonify({'error': 'Cérémonie non trouvée'}), 404
        
        ceremony_name = ceremony.ceremony_name
        db.session.delete(ceremony)
        db.session.commit()
        
        return jsonify({'message': f'Cérémonie "{ceremony_name}" supprimée avec succès'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/organizer/<int:organizer_id>', methods=['GET'])
def get_ceremonies_by_organizer(organizer_id):
    """Récupérer toutes les cérémonies d'un organisateur"""
    try:
        ceremonies = CeremonyBuffet.query.filter_by(organizer_person_id=organizer_id).join(Food).all()
        
        result = []
        for ceremony in ceremonies:
            total_cost = ceremony.cost_per_unit * ceremony.quantity_needed if ceremony.cost_per_unit else None
            result.append({
                'id': ceremony.id,
                'ceremony_name': ceremony.ceremony_name,
                'ceremony_date': ceremony.ceremony_date.isoformat(),
                'expected_guests': ceremony.expected_guests,
                'food_name': ceremony.food.name,
                'total_cost': total_cost,
                'is_confirmed': ceremony.is_confirmed
            })
        
        return jsonify({
            'organizer_id': organizer_id,
            'ceremonies': result,
            'total_ceremonies': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/budget-analysis', methods=['GET'])
def budget_analysis():
    """Analyse des coûts des cérémonies"""
    try:
        # Statistiques globales
        total_ceremonies = CeremonyBuffet.query.count()
        confirmed_ceremonies = CeremonyBuffet.query.filter_by(is_confirmed=True).count()
        
        # Coûts moyens
        avg_cost = db.session.query(func.avg(CeremonyBuffet.cost_per_unit * CeremonyBuffet.quantity_needed)).scalar()
        avg_guests = db.session.query(func.avg(CeremonyBuffet.expected_guests)).scalar()
        
        # Cérémonies les plus coûteuses
        expensive_ceremonies = db.session.query(
            CeremonyBuffet.ceremony_name,
            CeremonyBuffet.expected_guests,
            (CeremonyBuffet.cost_per_unit * CeremonyBuffet.quantity_needed).label('total_cost')
        ).filter(CeremonyBuffet.cost_per_unit.isnot(None)).order_by(
            (CeremonyBuffet.cost_per_unit * CeremonyBuffet.quantity_needed).desc()
        ).limit(5).all()
        
        return jsonify({
            'total_ceremonies': total_ceremonies,
            'confirmed_ceremonies': confirmed_ceremonies,
            'pending_ceremonies': total_ceremonies - confirmed_ceremonies,
            'average_total_cost': float(avg_cost) if avg_cost else None,
            'average_guests': float(avg_guests) if avg_guests else None,
            'most_expensive_ceremonies': [
                {
                    'name': ceremony.ceremony_name,
                    'guests': ceremony.expected_guests,
                    'total_cost': float(ceremony.total_cost)
                } for ceremony in expensive_ceremonies
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ceremony_buffet_bp.route('/<int:ceremony_id>/confirm', methods=['POST'])
def confirm_ceremony(ceremony_id):
    """Confirmer une cérémonie"""
    try:
        ceremony = CeremonyBuffet.query.get(ceremony_id)
        if not ceremony:
            return jsonify({'error': 'Cérémonie non trouvée'}), 404
        
        ceremony.is_confirmed = True
        db.session.commit()
        
        return jsonify({
            'id': ceremony.id,
            'ceremony_name': ceremony.ceremony_name,
            'is_confirmed': ceremony.is_confirmed,
            'message': 'Cérémonie confirmée avec succès'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
