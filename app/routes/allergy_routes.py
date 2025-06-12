from flask import Blueprint, request, jsonify
from app import db
from app.models import Allergy, Person, Ingredient

allergy_bp = Blueprint('allergy_bp', __name__)

@allergy_bp.route('/', methods=['GET'])
def get_all_allergies():
    allergies = Allergy.query.all()
    return jsonify([{
        'id': a.id,
        'person_id': a.person_id,
        'person_name': a.person.name,
        'ingredient_id': a.ingredient_id,
        'ingredient_name': a.ingredient.name
    } for a in allergies])

@allergy_bp.route('/', methods=['POST'])
def create_allergy():
    data = request.json
    
    # Vérifier si la personne existe
    person = Person.query.get(data['person_id'])
    if not person:
        return jsonify({'error': 'Person not found'}), 404
    
    # Vérifier si l'ingrédient existe
    ingredient = Ingredient.query.get(data['ingredient_id'])
    if not ingredient:
        return jsonify({'error': 'Ingredient not found'}), 404
    
    # Vérifier si l'allergie existe déjà
    existing_allergy = Allergy.query.filter_by(
        person_id=data['person_id'], 
        ingredient_id=data['ingredient_id']
    ).first()
    
    if existing_allergy:
        return jsonify({'error': 'Allergy already exists'}), 400
    
    allergy = Allergy(person_id=data['person_id'], ingredient_id=data['ingredient_id'])
    db.session.add(allergy)
    db.session.commit()
    return jsonify({'message': 'Allergy created', 'id': allergy.id}), 201

@allergy_bp.route('/<int:allergy_id>', methods=['GET'])
def get_allergy(allergy_id):
    allergy = Allergy.query.get_or_404(allergy_id)
    return jsonify({
        'id': allergy.id,
        'person_id': allergy.person_id,
        'person_name': allergy.person.name,
        'ingredient_id': allergy.ingredient_id,
        'ingredient_name': allergy.ingredient.name
    })

@allergy_bp.route('/<int:allergy_id>', methods=['DELETE'])
def delete_allergy(allergy_id):
    allergy = Allergy.query.get_or_404(allergy_id)
    db.session.delete(allergy)
    db.session.commit()
    return jsonify({'message': 'Allergy deleted'})
