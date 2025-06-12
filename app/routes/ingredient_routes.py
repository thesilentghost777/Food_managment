from flask import Blueprint, request, jsonify
from app import db
from app.models import Ingredient

ingredient_bp = Blueprint('ingredient_bp', __name__)

@ingredient_bp.route('/', methods=['GET'])
def get_all_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([{
        'id': i.id,
        'food_id': i.food_id,
        'name': i.name,
        'description': i.description,
        'is_allergen': i.is_allergen
    } for i in ingredients])

@ingredient_bp.route('/', methods=['POST'])
def create_ingredient():
    data = request.json
    ingredient = Ingredient(
        food_id=data['food_id'],
        name=data['name'],
        description=data.get('description'),
        is_allergen=data.get('is_allergen', False)
    )
    db.session.add(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient created', 'id': ingredient.id}), 201

@ingredient_bp.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    return jsonify({
        'id': ingredient.id,
        'food_id': ingredient.food_id,
        'name': ingredient.name,
        'description': ingredient.description,
        'is_allergen': ingredient.is_allergen
    })

@ingredient_bp.route('/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    data = request.json
    ingredient.name = data.get('name', ingredient.name)
    ingredient.description = data.get('description', ingredient.description)
    ingredient.is_allergen = data.get('is_allergen', ingredient.is_allergen)
    db.session.commit()
    return jsonify({'message': 'Ingredient updated'})

@ingredient_bp.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient deleted'})
