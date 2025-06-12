from flask import Blueprint, request, jsonify
from app import db
from app.models import Food

food_bp = Blueprint('food_bp', __name__)

@food_bp.route('/', methods=['GET'])
def get_all_foods():
    foods = Food.query.all()
    return jsonify([{'id': f.id, 'name': f.name, 'description': f.description} for f in foods])

@food_bp.route('/', methods=['POST'])
def create_food():
    data = request.json
    food = Food(name=data['name'], description=data.get('description'))
    db.session.add(food)
    db.session.commit()
    return jsonify({'message': 'Food created', 'id': food.id}), 201

@food_bp.route('/<int:food_id>', methods=['GET'])
def get_food(food_id):
    food = Food.query.get_or_404(food_id)
    return jsonify({
        'id': food.id,
        'name': food.name,
        'description': food.description
    })

@food_bp.route('/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    food = Food.query.get_or_404(food_id)
    data = request.json
    food.name = data.get('name', food.name)
    food.description = data.get('description', food.description)
    db.session.commit()
    return jsonify({'message': 'Food updated'})

@food_bp.route('/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    return jsonify({'message': 'Food deleted'})

@food_bp.route('/<int:food_id>/ingredients', methods=['GET'])
def get_food_ingredients(food_id):
    food = Food.query.get_or_404(food_id)
    ingredients = [{
        'id': ingredient.id,
        'name': ingredient.name,
        'description': ingredient.description,
        'is_allergen': ingredient.is_allergen
    } for ingredient in food.ingredients]
    return jsonify(ingredients)
