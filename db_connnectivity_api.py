import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging

# Configuration de la base de données
DB_CONFIG = {
    'host': 'localhost',
    'database': 'food_management',
    'user': 'ghost',
    'password': 'ghost',
    'port': 5432
}

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """Context manager pour gérer les connexions à la base de données"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Erreur de base de données: {e}")
        raise
    finally:
        if conn:
            conn.close()

# ============================================================================
# CRUD OPERATIONS FOR PERSON TABLE
# ============================================================================

class PersonCRUD:
    
    @staticmethod
    def create_person(name, age, sexe):
        """Créer une nouvelle personne"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO person (name, age, sexe) 
                VALUES (%s, %s, %s) 
                RETURNING id, name, age, sexe;
            """
            cursor.execute(query, (name, age, sexe))
            result = cursor.fetchone()
            conn.commit()
            return {
                'id': result[0],
                'name': result[1],
                'age': result[2],
                'sexe': result[3]
            }
    
    @staticmethod
    def get_person(person_id):
        """Récupérer une personne par ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM person WHERE id = %s;"
            cursor.execute(query, (person_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_all_persons():
        """Récupérer toutes les personnes"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM person ORDER BY id;"
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def update_person(person_id, name=None, age=None, sexe=None):
        """Mettre à jour une personne"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Construire la requête dynamiquement
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if age is not None:
                updates.append("age = %s")
                params.append(age)
            if sexe is not None:
                updates.append("sexe = %s")
                params.append(sexe)
            
            if not updates:
                return None
            
            params.append(person_id)
            query = f"""
                UPDATE person 
                SET {', '.join(updates)} 
                WHERE id = %s 
                RETURNING *;
            """
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            return dict(result) if result else None
    
    @staticmethod
    def delete_person(person_id):
        """Supprimer une personne"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM person WHERE id = %s RETURNING id;"
            cursor.execute(query, (person_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None

# ============================================================================
# CRUD OPERATIONS FOR FOOD TABLE
# ============================================================================

class FoodCRUD:
    
    @staticmethod
    def create_food(name, description=None):
        """Créer un nouveau plat"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO food (name, description) 
                VALUES (%s, %s) 
                RETURNING id, name, description;
            """
            cursor.execute(query, (name, description))
            result = cursor.fetchone()
            conn.commit()
            return {
                'id': result[0],
                'name': result[1],
                'description': result[2]
            }
    
    @staticmethod
    def get_food(food_id):
        """Récupérer un plat par ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM food WHERE id = %s;"
            cursor.execute(query, (food_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_all_foods():
        """Récupérer tous les plats"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM food ORDER BY id;"
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def update_food(food_id, name=None, description=None):
        """Mettre à jour un plat"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            
            if not updates:
                return None
            
            params.append(food_id)
            query = f"""
                UPDATE food 
                SET {', '.join(updates)} 
                WHERE id = %s 
                RETURNING *;
            """
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            return dict(result) if result else None
    
    @staticmethod
    def delete_food(food_id):
        """Supprimer un plat"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM food WHERE id = %s RETURNING id;"
            cursor.execute(query, (food_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None

# ============================================================================
# CRUD OPERATIONS FOR INGREDIENT TABLE
# ============================================================================

class IngredientCRUD:
    
    @staticmethod
    def create_ingredient(food_id, name, description=None, is_allergen=False):
        """Créer un nouveau ingrédient"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO ingredient (food_id, name, description, is_allergen) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id, food_id, name, description, is_allergen;
            """
            cursor.execute(query, (food_id, name, description, is_allergen))
            result = cursor.fetchone()
            conn.commit()
            return {
                'id': result[0],
                'food_id': result[1],
                'name': result[2],
                'description': result[3],
                'is_allergen': result[4]
            }
    
    @staticmethod
    def get_ingredient(ingredient_id):
        """Récupérer un ingrédient par ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT i.*, f.name as food_name 
                FROM ingredient i 
                JOIN food f ON i.food_id = f.id 
                WHERE i.id = %s;
            """
            cursor.execute(query, (ingredient_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_all_ingredients():
        """Récupérer tous les ingrédients"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT i.*, f.name as food_name 
                FROM ingredient i 
                JOIN food f ON i.food_id = f.id 
                ORDER BY i.id;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def get_ingredients_by_food(food_id):
        """Récupérer les ingrédients d'un plat spécifique"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM ingredient WHERE food_id = %s ORDER BY id;"
            cursor.execute(query, (food_id,))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def update_ingredient(ingredient_id, food_id=None, name=None, description=None, is_allergen=None):
        """Mettre à jour un ingrédient"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            updates = []
            params = []
            
            if food_id is not None:
                updates.append("food_id = %s")
                params.append(food_id)
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            if is_allergen is not None:
                updates.append("is_allergen = %s")
                params.append(is_allergen)
            
            if not updates:
                return None
            
            params.append(ingredient_id)
            query = f"""
                UPDATE ingredient 
                SET {', '.join(updates)} 
                WHERE id = %s 
                RETURNING *;
            """
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.commit()
            return dict(result) if result else None
    
    @staticmethod
    def delete_ingredient(ingredient_id):
        """Supprimer un ingrédient"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM ingredient WHERE id = %s RETURNING id;"
            cursor.execute(query, (ingredient_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None

# ============================================================================
# CRUD OPERATIONS FOR ALLERGY TABLE
# ============================================================================

class AllergyCRUD:
    
    @staticmethod
    def create_allergy(person_id, ingredient_id):
        """Créer une nouvelle allergie"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                query = """
                    INSERT INTO allergy (person_id, ingredient_id) 
                    VALUES (%s, %s) 
                    RETURNING id, person_id, ingredient_id;
                """
                cursor.execute(query, (person_id, ingredient_id))
                result = cursor.fetchone()
                conn.commit()
                return {
                    'id': result[0],
                    'person_id': result[1],
                    'ingredient_id': result[2]
                }
            except psycopg2.IntegrityError:
                conn.rollback()
                raise ValueError("Cette allergie existe déjà pour cette personne")
    
    @staticmethod
    def get_allergy(allergy_id):
        """Récupérer une allergie par ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT a.*, p.name as person_name, i.name as ingredient_name 
                FROM allergy a 
                JOIN person p ON a.person_id = p.id 
                JOIN ingredient i ON a.ingredient_id = i.id 
                WHERE a.id = %s;
            """
            cursor.execute(query, (allergy_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_all_allergies():
        """Récupérer toutes les allergies"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT a.*, p.name as person_name, i.name as ingredient_name 
                FROM allergy a 
                JOIN person p ON a.person_id = p.id 
                JOIN ingredient i ON a.ingredient_id = i.id 
                ORDER BY a.id;
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def get_allergies_by_person(person_id):
        """Récupérer les allergies d'une personne"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT a.*, i.name as ingredient_name, i.description as ingredient_description 
                FROM allergy a 
                JOIN ingredient i ON a.ingredient_id = i.id 
                WHERE a.person_id = %s 
                ORDER BY i.name;
            """
            cursor.execute(query, (person_id,))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def get_people_allergic_to_ingredient(ingredient_id):
        """Récupérer les personnes allergiques à un ingrédient"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = """
                SELECT a.*, p.name as person_name, p.age, p.sexe 
                FROM allergy a 
                JOIN person p ON a.person_id = p.id 
                WHERE a.ingredient_id = %s 
                ORDER BY p.name;
            """
            cursor.execute(query, (ingredient_id,))
            results = cursor.fetchall()
            return [dict(row) for row in results]
    
    @staticmethod
    def delete_allergy(allergy_id):
        """Supprimer une allergie"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM allergy WHERE id = %s RETURNING id;"
            cursor.execute(query, (allergy_id,))
            result = cursor.fetchone()
            conn.commit()
            return result is not None
    
    @staticmethod
    def delete_allergy_by_person_ingredient(person_id, ingredient_id):
        """Supprimer une allergie par person_id et ingredient_id"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = "DELETE FROM allergy WHERE person_id = %s AND ingredient_id = %s RETURNING id;"
            cursor.execute(query, (person_id, ingredient_id))
            result = cursor.fetchone()
            conn.commit()
            return result is not None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def check_database_connection():
    """Vérifier la connexion à la base de données"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            return True
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données: {e}")
        return False

def get_database_stats():
    """Obtenir des statistiques sur la base de données"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        stats = {}
        
        tables = ['person', 'food', 'ingredient', 'allergy']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            stats[table] = cursor.fetchone()[0]
        
        return stats


