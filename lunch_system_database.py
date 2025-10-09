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
            search_term: Sökterm för livsmedel (t.ex. "pasta", "chicken", "vegetables")
            
        Returns:
            Dict med resultat av import (added, skipped, errors)
        """
        try:
            # Import här för att undvika cirkulära imports
            from skolmaten_api import search_food_ingredients
            
            # Hämta ENDAST livsmedel från Open Food Facts (inga recept)
            food_products = search_food_ingredients(search_term)
            
            # Använd endast food products, INGA recept
            all_meals = food_products
            
            if not all_meals:
                return {"error": f"Inga måltider hittades för '{search_term}'", "added": 0, "skipped": 0}
            
            # Importera måltiderna till databasen
            added = 0
            skipped = 0
            errors = []
            
            for meal_data in all_meals:
                try:
                    # Kontrollera om måltiden redan finns
                    existing = self.db.execute(
                        "SELECT id FROM meals WHERE name = ?",
                        (meal_data.get("name", ""),)
                    )
                    
                    if existing:
                        skipped += 1
                    else:
                        # Lägg till måltiden
                        meal_info = {
                            "name": meal_data.get("name", ""),
                            "description": meal_data.get("description", ""),
                            "price": meal_data.get("price", 0.0),
                            "category": meal_data.get("category", "Huvudrätt")
                        }
                        
                        self.add_meal(meal_info)
                        added += 1
                        
                except Exception as e:
                    errors.append(f"Fel vid import av {meal_data.get('name', 'okänd måltid')}: {str(e)}")
            
            result = {
                "added": added,
                "skipped": skipped,
                "search_term": search_term,
                "total_found": len(all_meals),
                "sources": "Open Food Facts + TheMealDB"
            }
            
            if errors:
                result["errors"] = errors
            
            return result
            
        except ImportError:
            return {"error": "Food API-moduler kunde inte importeras", "added": 0, "skipped": 0}
        except Exception as e:
            return {"error": f"Oväntat fel: {str(e)}", "added": 0, "skipped": 0}
