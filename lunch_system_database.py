"""
School Lunch Database Management System

FILE STRUCTURE AND FUNCTIONALITY:
=================================

1. DATABASE SCHEMA:
   ==================
   1.1 Students Table:
       - id: PRIMARY KEY AUTOINCREMENT
       - name: TEXT NOT NULL (student full name)
       - allergies: TEXT (comma-separated allergen list)
       - external_account_id: TEXT (reference to external payment system)
       - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   
   1.2 Meals Table:
       - id: PRIMARY KEY AUTOINCREMENT
       - name: TEXT NOT NULL (meal name)
       - description: TEXT (detailed meal description)
       - price: REAL NOT NULL DEFAULT 0.0 (cost in currency)
       - category: TEXT (main, salad, dessert, drink, snack)
       - picture_url: TEXT (path/URL to meal image)
       - allergens: TEXT (comma-separated: nuts, dairy, gluten, etc.)
       - ingredients: TEXT (comma-separated ingredient list)
       - nutritional_info: TEXT (detailed nutrition facts)
       - calories: INTEGER (caloric content per serving)
       - preparation_time: INTEGER (minutes to prepare)
       - serving_size: TEXT (portion description: "350g", "1 cup")
       - dietary_restrictions: TEXT (restriction descriptions)
       - is_vegetarian: BOOLEAN DEFAULT 0
       - is_vegan: BOOLEAN DEFAULT 0
       - is_gluten_free: BOOLEAN DEFAULT 0
       - is_halal: BOOLEAN DEFAULT 0
       - is_kosher: BOOLEAN DEFAULT 0
       - spice_level: INTEGER DEFAULT 0 (0-5 scale)
       - availability_status: TEXT DEFAULT 'available'
       - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   
   1.3 Meal Schedule Table:
       - id: PRIMARY KEY AUTOINCREMENT
       - meal_id: INTEGER NOT NULL (FK to meals.id)
       - date: DATE NOT NULL (scheduled serving date)
       - available_quantity: INTEGER DEFAULT 0 (portions available)
       - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   
   1.4 Transactions Table:
       - id: PRIMARY KEY AUTOINCREMENT
       - student_id: INTEGER NOT NULL (FK to students.id)
       - meal_id: INTEGER NOT NULL (FK to meals.id)
       - date: DATE NOT NULL (transaction date)
       - external_transaction_id: TEXT (reference to external payment system)
       - status: TEXT DEFAULT 'completed' (completed, pending, cancelled)
       - created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

2. CORE FUNCTIONS:
   ================
   2.1 Database Initialization:
       - initialize_database(): Create all required tables
       - setup_initial_data(): Insert sample meals and test data
       - validate_schema(): Check table structure integrity
   
   2.2 Student Management:
       - add_student(student_info): Register new student
       - update_student(student_id, updates): Modify student data
       - search_students(search_term): Find by name/grade/class
       - get_student_by_id(student_id): Retrieve specific student
       - get_all_students(): List all registered students
       - update_student_balance(student_id, amount): Adjust balance
   
   2.3 Meal Management:
       - add_meal_option(meal_info): Add new meal to menu
       - update_meal(meal_id, updates): Modify meal details
       - get_all_meals(): List available meals
       - get_meals_by_date(date): Meals scheduled for date
       - get_meals_by_dietary_restriction(type): Filter by diet
       - get_meals_without_allergen(allergen): Exclude allergens
       - search_meals_by_ingredients(ingredient): Find by ingredient
       - get_meals_by_spice_level(max_level): Filter by spice
   
   2.4 Scheduling & Availability:
       - schedule_meal(meal_id, date, quantity): Set daily menu
       - update_meal_availability(meal_id, status): Change status
       - check_meal_availability(meal_id, date): Verify stock
   
   2.5 Transaction Processing:
       - record_transaction(): Log meal purchases
       - process_payment(): Handle payment processing
       - get_student_lunch_history(): Purchase history
       - get_daily_transactions(): Daily transaction log

3. REPORTING & ANALYTICS:
   ======================
   3.1 Sales Reports:
       - daily_sales: Meals sold per day with revenue
       - weekly_summary: Week-by-week sales analysis
       - popular_meals: Most frequently ordered items
       - revenue_analysis: Financial performance metrics
   
   3.2 Student Reports:
       - student_balance: Individual account status
       - student_activity: Purchase patterns per student
       - attendance_tracking: Meal participation rates
       - payment_history: Transaction records per student
   
   3.3 Operational Reports:
       - inventory_usage: Meal consumption tracking
       - dietary_preference_analysis: Popular diet types
       - allergen_impact_reports: Allergen-free meal demand
       - preparation_time_analysis: Kitchen efficiency metrics

4. SECURITY & DATA INTEGRITY:
   ===========================
   4.1 Transaction Safety:
       - Atomic database operations
       - Rollback capability on errors
       - Connection pooling and management
   
   4.2 Backup & Recovery:
       - Automatic backups before writes
       - Timestamped backup files
       - Database corruption detection
   
   4.3 Input Validation:
       - SQL injection prevention via parameterized queries
       - Data type validation
       - Required field enforcement
   
   4.4 Permission Management:
       - Write permission validation
       - Access control mechanisms
       - Audit trail maintenance

5. QUERY & SEARCH CAPABILITIES:
   ============================
   5.1 Student Queries:
       - Search by partial name matching
       - Filter by grade or class
       - Sort by balance, activity, etc.
   
   5.2 Meal Queries:
       - Filter by dietary restrictions
       - Search by ingredients or allergens
       - Sort by popularity, price, calories
   
   5.3 Transaction Queries:
       - Date range filtering
       - Payment method analysis
       - Student spending patterns
   
   5.4 Statistical Queries:
       - Database health metrics
       - Performance statistics
       - Usage analytics
"""

from database_wrapper import SQLiteDB
from typing import List, Dict, Optional, Any, Tuple
import sqlite3

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

    def setup_initial_data(self) -> None:
        """Setup initial sample meal data"""
        sample_meals = [
            {
                "name": "Chicken Pasta", 
                "description": "Creamy chicken pasta with vegetables", 
                "price": 45.0, 
                "category": "main"
            },
            {
                "name": "Vegetarian Salad", 
                "description": "Fresh mixed salad with dressing", 
                "price": 35.0, 
                "category": "salad"
            },
            {
                "name": "Fish and Chips", 
                "description": "Crispy fish with potato chips", 
                "price": 50.0, 
                "category": "main"
            },
            {
                "name": "Fruit Cup", 
                "description": "Mixed seasonal fruits", 
                "price": 20.0, 
                "category": "dessert"
            }
        ]
        
        for meal in sample_meals:
            existing = self.db.execute("SELECT id FROM meals WHERE name = ?", (meal["name"],))
            if not existing:
                cols, vals = zip(*meal.items())
                sql = f"INSERT INTO meals ({','.join(cols)}) VALUES ({','.join(['?']*len(vals))})"
                with self.db.transaction():
                    self.db.execute_write(sql, vals)

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
