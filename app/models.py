from app import db
from datetime import datetime

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sexe = db.Column(db.String(10), nullable=False)
    allergies = db.relationship('Allergy', back_populates='person', cascade='all, delete-orphan')
    consumptions = db.relationship('Consumption', back_populates='person', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Person {self.name}>"

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.relationship('Ingredient', back_populates='food', cascade='all, delete-orphan')
    consumptions = db.relationship('Consumption', back_populates='food', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Food {self.name}>"

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_allergen = db.Column(db.Boolean, default=False)
    food = db.relationship('Food', back_populates='ingredients')
    allergies = db.relationship('Allergy', back_populates='ingredient', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Ingredient {self.name}>"

class Allergy(db.Model):
    __tablename__ = 'allergy'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'), nullable=False)
    person = db.relationship('Person', back_populates='allergies')
    ingredient = db.relationship('Ingredient', back_populates='allergies')
    __table_args__ = (db.UniqueConstraint('person_id', 'ingredient_id', name='_person_ingredient_uc'),)
    
    def __repr__(self):
        return f"<Allergy Person {self.person_id} - Ingredient {self.ingredient_id}>"

class Consumption(db.Model):
    __tablename__ = 'consumption'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id', ondelete='CASCADE'), nullable=False)
    consumption_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    had_problem = db.Column(db.Boolean, default=False)
    problem_details = db.Column(db.Text)
    severity_level = db.Column(db.String(20))  # 'mild', 'moderate', 'severe'
    symptoms = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Relations
    person = db.relationship('Person', back_populates='consumptions')
    food = db.relationship('Food', back_populates='consumptions')
    
    def __repr__(self):
        return f"<Consumption Person {self.person_id} - Food {self.food_id} - Problem: {self.had_problem}>"

# Ajout à models.py - 2 nouvelles tables

class WeeklyMealPlan(db.Model):
    __tablename__ = 'weekly_meal_plan'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)  # Lundi de la semaine
    day_of_week = db.Column(db.Integer, nullable=False)  # 1=Lundi, 7=Dimanche
    meal_type = db.Column(db.String(20), nullable=False)  # 'breakfast', 'lunch', 'dinner', 'snack'
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    is_prepared = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    person = db.relationship('Person')
    food = db.relationship('Food')
    
    __table_args__ = (db.UniqueConstraint('person_id', 'week_start_date', 'day_of_week', 'meal_type', 'food_id', name='_meal_plan_uc'),)
    
    def __repr__(self):
        return f"<WeeklyMealPlan {self.person_id} - Week {self.week_start_date} - Day {self.day_of_week}>"

class CeremonyBuffet(db.Model):
    __tablename__ = 'ceremony_buffet'
    id = db.Column(db.Integer, primary_key=True)
    ceremony_name = db.Column(db.String(200), nullable=False)
    ceremony_date = db.Column(db.DateTime, nullable=False)
    organizer_person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    expected_guests = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200))
    budget = db.Column(db.Float)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity_needed = db.Column(db.Integer, nullable=False)
    cost_per_unit = db.Column(db.Float)
    is_confirmed = db.Column(db.Boolean, default=False)
    special_requirements = db.Column(db.Text)  # Allergies, préférences, etc.
    supplier_info = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    organizer = db.relationship('Person')
    food = db.relationship('Food')
    
    def __repr__(self):
        return f"<CeremonyBuffet {self.ceremony_name} - {self.ceremony_date}>"
        
