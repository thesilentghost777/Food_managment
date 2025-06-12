from flask import Blueprint, request, jsonify
from app import db
from app.models import Person

person_bp = Blueprint('person_bp', __name__)

@person_bp.route('/', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'age': p.age, 'sexe': p.sexe} for p in persons])

@person_bp.route('/', methods=['POST'])
def create_person():
    data = request.json
    person = Person(name=data['name'], age=data['age'], sexe=data['sexe'])
    db.session.add(person)
    db.session.commit()
    return jsonify({'message': 'Person created', 'id': person.id}), 201

@person_bp.route('/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get_or_404(person_id)
    return jsonify({
        'id': person.id,
        'name': person.name,
        'age': person.age,
        'sexe': person.sexe
    })

@person_bp.route('/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    person = Person.query.get_or_404(person_id)
    data = request.json
    person.name = data.get('name', person.name)
    person.age = data.get('age', person.age)
    person.sexe = data.get('sexe', person.sexe)
    db.session.commit()
    return jsonify({'message': 'Person updated'})

@person_bp.route('/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'Person deleted'})

@person_bp.route('/<int:person_id>/allergies', methods=['GET'])
def get_person_allergies(person_id):
    person = Person.query.get_or_404(person_id)
    allergies = [{
        'id': allergy.id,
        'ingredient_id': allergy.ingredient_id,
        'ingredient_name': allergy.ingredient.name
    } for allergy in person.allergies]
    return jsonify(allergies)
