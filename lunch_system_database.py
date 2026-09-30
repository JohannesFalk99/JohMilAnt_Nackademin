from database_wrapper import SQLiteDB
from typing import List, Dict, Optional, Any, Tuple
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class SchoolLunchDB:
    def __init__(self, db_path: str) -> None:
        self.db: SQLiteDB = SQLiteDB(db_path)
        self.initialize_database()

    def initialize_database(self) -> None:
        """Create the basic tables if they don't exist"""
        with self.db.transaction():
            self.db.execute_write("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    grade TEXT,
                    class TEXT,
                    allergies TEXT,
                    external_account_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.db.execute_write("""
                CREATE TABLE IF NOT EXISTS meals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL DEFAULT 0.0,
                    category TEXT,
                    rating REAL DEFAULT 0.0,
                    rating_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.db.execute_write("""
                CREATE TABLE IF NOT EXISTS meal_schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    meal_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    available_quantity INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (meal_id) REFERENCES meals (id)
                )
            """)

            self.db.execute_write("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    meal_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (id),
                    FOREIGN KEY (meal_id) REFERENCES meals (id)
                )
            """)

            self.db.execute_write("""
                CREATE TABLE IF NOT EXISTS student_credentials (
                    student_id INTEGER PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (id)
                )
            """)

    def set_student_password(self, student_id: int, password: str) -> None:
        if len(password) < 12:
            raise ValueError('Use a password with at least 12 characters')
        if not self.db.execute('SELECT id FROM students WHERE id = ?', (student_id,)):
            raise ValueError('Student not found')
        self.db.execute_write(
            'INSERT INTO student_credentials (student_id, password_hash) VALUES (?, ?) '
            'ON CONFLICT(student_id) DO UPDATE SET password_hash = excluded.password_hash',
            (student_id, generate_password_hash(password)),
        )

    def authenticate_student(self, name: str, password: str):
        students = self.db.execute(
            'SELECT s.id, s.name, c.password_hash FROM students s '
            'JOIN student_credentials c ON c.student_id = s.id '
            'WHERE LOWER(s.name) = LOWER(?)', (name,)
        )
        # Duplicate names must be resolved before allowing login.
        if len(students) != 1:
            return None
        student = students[0]
        if check_password_hash(student['password_hash'], password):
            return student
        return None

    # --- BASIC OPERATIONS ---

    def add_student(self, student_info: Dict[str, Any]) -> Optional[int]:
        cols, vals = zip(*student_info.items())
        sql = f"INSERT INTO students ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
        with self.db.transaction():
            return self.db.execute_write(sql, vals)

    def add_meal(self, meal_info: Dict[str, Any]) -> Optional[int]:
        cols, vals = zip(*meal_info.items())
        sql = f"INSERT INTO meals ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
        with self.db.transaction():
            return self.db.execute_write(sql, vals)

    def schedule_meal(self, meal_id: int, date: str, quantity: int = 0) -> Optional[int]:
        sql = "INSERT INTO meal_schedule (meal_id, date, available_quantity) VALUES (?, ?, ?)"
        with self.db.transaction():
            return self.db.execute_write(sql, (meal_id, date, quantity))

    def record_transaction(self, student_id: int, meal_id: int, date: str) -> Optional[int]:
        sql = "INSERT INTO transactions (student_id, meal_id, date) VALUES (?, ?, ?)"
        with self.db.transaction():
            return self.db.execute_write(sql, (student_id, meal_id, date))

    # --- BASIC QUERIES ---

    def get_all_students(self) -> None:
        self.db.execute("SELECT * FROM students ORDER BY name")
        #print all students
        print(self.db.execute("SELECT * FROM students ORDER BY name"))
        return 

    def get_all_meals(self) -> List[sqlite3.Row]:
        return self.db.execute("SELECT * FROM meals ORDER BY name")

    def get_meals_by_date(self, date: str) -> List[sqlite3.Row]:
        sql = """SELECT m.*, ms.available_quantity 
                 FROM meals m
                 JOIN meal_schedule ms ON m.id = ms.meal_id
                 WHERE ms.date = ?
                 ORDER BY m.name"""
        return self.db.execute(sql, (date,))

    def get_student_transactions(self, student_id: int) -> List[sqlite3.Row]:
        sql = """SELECT t.*, m.name as meal_name
                 FROM transactions t
                 JOIN meals m ON t.meal_id = m.id
                 WHERE t.student_id = ?
                 ORDER BY t.date DESC"""
        return self.db.execute(sql, (student_id,))

    def rate_meal(self, meal_id: int, rating: float) -> bool:
        """Add a rating to a meal (1-5 stars) and update average"""
        # Get current rating info
        meal = self.db.execute("SELECT rating, rating_count FROM meals WHERE id = ?", (meal_id,))
        if not meal:
            return False
        
        current_rating, current_count = meal[0]
        
        # Calculate new average rating
        total_rating = (current_rating * current_count) + rating
        new_count = current_count + 1
        new_average = total_rating / new_count
        
        # Update meal with new rating
        sql = "UPDATE meals SET rating = ?, rating_count = ? WHERE id = ?"
        with self.db.transaction():
            self.db.execute_write(sql, (new_average, new_count, meal_id))
        return True



    def import_menu_from_json(self, json_file_path: str = "menu.json") -> Dict[str, Any]:
        """Import meals from JSON file (replaces api_fetch.py functionality)"""
        import json
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return {"error": f"File {json_file_path} not found"}
        except json.JSONDecodeError:
            return {"error": f"Invalid JSON in {json_file_path}"}

        meals = data.get("meals", [])
        if not meals:
            return {"error": "No meals found in JSON"}

        added = 0
        skipped = 0

        for meal_data in meals:
            # Check if meal already exists
            existing = self.db.execute(
                "SELECT id FROM meals WHERE name = ? AND category = ?",
                (meal_data.get("name", ""), meal_data.get("type", ""))
            )
            
            if existing:
                skipped += 1
            else:
                # Map JSON format to our database format
                meal = {
                    "name": meal_data.get("name", ""),
                    "description": meal_data.get("name", ""),  # Use name as description if not provided
                    "price": meal_data.get("price", 0.0),
                    "category": meal_data.get("type", "main")
                }
                
                cols, vals = zip(*meal.items())
                sql = f"INSERT INTO meals ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
                with self.db.transaction():
                    self.db.execute_write(sql, vals)
                added += 1

        return {"added": added, "skipped": skipped}

    def import_meals_from_openfoodfacts(self, search_term: str = "pasta") -> Dict[str, Any]:
        """
        Hämta och importera livsmedel från Open Food Facts API (INGA RECEPT)
        
        Args:
            search_term: Sökterm för livsmedel (t.ex. "pasta", …3333 tokens truncated…render_template('dashboard.html', username=session['username'])

@app.route('/api/meals')
def get_meals():
    if not is_authenticated():
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        meals = db.get_all_meals()
        meals_list = []
        
        if meals:  # Check if meals is not None
            for meal in meals:
                meals_list.append({
                    'id': meal[0],
                    'name': meal[1],
                    'description': meal[2],
                    'price': meal[3],
                    'category': meal[4],
                    'rating': round(meal[5], 1) if meal[5] else 0.0,  # meal[5] is rating
                    'rating_count': meal[6] if meal[6] else 0  # meal[6] is rating_count
                })
        
        return jsonify(meals_list)
    except Exception as e:
        app.logger.exception('Failed to load meals')
        return jsonify({'error': 'Failed to load meals'}), 500

@app.route('/api/order', methods=['POST'])
def order_meal():
    if not is_authenticated():
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    meal_id = data.get('meal_id')
    
    if not meal_id:
        return jsonify({'error': 'No meal selected'}), 400
    
    # Record the transaction
    student_id = session.get('student_id')
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        transaction_id = db.record_transaction(student_id, meal_id, today)
        return jsonify({'success': True, 'message': 'Order placed successfully!'})
    except Exception as e:
        return jsonify({'error': 'Failed to place order'}), 500

@app.route('/api/rate', methods=['POST'])
def rate_meal():
    if not is_authenticated():
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    meal_id = data.get('meal_id')
    rating = data.get('rating')
    
    if not meal_id or not rating:
        return jsonify({'error': 'Missing meal ID or rating'}), 400
    
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    success = db.rate_meal(meal_id, rating)
    if success:
        return jsonify({'success': True, 'message': 'Rating submitted!'})
    else:
        return jsonify({'error': 'Failed to submit rating'}), 500

@app.route('/api/import-openfoodfacts', methods=['POST'])
def import_from_openfoodfacts():
    """Importera måltider från Open Food Facts API"""
    if not is_authenticated():
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    search_term = data.get('search_term', 'pasta')
    
    try:
        result = db.import_meals_from_openfoodfacts(search_term)
        
        if "error" in result:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'message': f"Importerade {result['added']} nya måltider för söktermen '{result['search_term']}'",
            'details': result
        })
    except Exception as e:
        return jsonify({'error': f'Import misslyckades: {str(e)}'}), 500

@app.route('/api/test-openfoodfacts')
def test_openfoodfacts():
    """Test-endpoint för att testa Open Food Facts API"""
    try:
        # Import här för att undvika problem om modulen inte finns
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from skolmaten_api import search_food_ingredients
        
        meals = search_food_ingredients("pasta")
        return jsonify({
            'success': True,
            'meals_found': len(meals),
            'sample_meals': meals[:3] if meals else []  # Visa första 3 som exempel
        })
    except ImportError:
        return jsonify({'error': 'Open Food Facts API inte tillgängligt'}), 500
    except Exception as e:
        return jsonify({'error': f'Test misslyckades: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1', host='127.0.0.1', port=5000)

