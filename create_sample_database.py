import os
import sys
import argparse
from datetime import datetime, timedelta
from lunch_system_database import SchoolLunchDB
from typing import List, Dict, Any

def create_sample_students() -> List[Dict[str, str]]:
    return [
        {"name": "Alice Johansson", "grade": "9", "class": "9A", "allergies": "nötter", "external_account_id": "student_001"},
        {"name": "Björn Svensson", "grade": "10", "class": "10B", "allergies": "ingen", "external_account_id": "student_002"},
        {"name": "Caroline Andersson", "grade": "9", "class": "9A", "allergies": "mjölk", "external_account_id": "student_003"},
        {"name": "David Nilsson", "grade": "11", "class": "11A", "allergies": "gluten", "external_account_id": "student_004"},
        {"name": "Emma Karlsson", "grade": "10", "class": "10A", "allergies": "skaldjur", "external_account_id": "student_005"},
        {"name": "Fredrik Eriksson", "grade": "9", "class": "9B", "allergies": "ingen", "external_account_id": "student_006"},
        {"name": "Greta Lindberg", "grade": "11", "class": "11B", "allergies": "ägg, soja", "external_account_id": "student_007"},
        {"name": "Henrik Persson", "grade": "10", "class": "10A", "allergies": "nötter, mjölk", "external_account_id": "student_008"},
        {"name": "Isabella Larsson", "grade": "9", "class": "9A", "allergies": "ingen", "external_account_id": "student_009"},
        {"name": "Jakob Olsson", "grade": "11", "class": "11A", "allergies": "gluten, ägg", "external_account_id": "student_010"},
        {"name": "Karin Gustafsson", "grade": "10", "class": "10B", "allergies": "fisk", "external_account_id": "student_011"},
        {"name": "Lukas Berg", "grade": "9", "class": "9B", "allergies": "ingen", "external_account_id": "student_012"},
        {"name": "Mia Granström", "grade": "11", "class": "11B", "allergies": "mjölk, nötter", "external_account_id": "student_013"},
        {"name": "Noah Holm", "grade": "10", "class": "10A", "allergies": "soja", "external_account_id": "student_014"},
        {"name": "Olivia Jonsson", "grade": "9", "class": "9A", "allergies": "ingen", "external_account_id": "student_015"},
        {"name": "Patrik Rodriguez", "grade": "11", "class": "11A", "allergies": "skaldjur, fisk", "external_account_id": "student_016"},
        {"name": "Quinn Adamsson", "grade": "10", "class": "10B", "allergies": "gluten", "external_account_id": "student_017"},
        {"name": "Ruben Mattsson", "grade": "9", "class": "9B", "allergies": "ägg", "external_account_id": "student_018"},
        {"name": "Samuel Cooper", "grade": "11", "class": "11B", "allergies": "ingen", "external_account_id": "student_019"},
        {"name": "Tara Bellman", "grade": "10", "class": "10A", "allergies": "nötter", "external_account_id": "student_020"},
        {"name": "Ulrika Patel", "grade": "9", "class": "9A", "allergies": "mjölk", "external_account_id": "student_021"},
        {"name": "Viktor Chen", "grade": "10", "class": "10B", "allergies": "ingen", "external_account_id": "student_022"},
        {"name": "Wendy Torres", "grade": "11", "class": "11A", "allergies": "nötter, soja", "external_account_id": "student_023"},
        {"name": "Xavier Kim", "grade": "9", "class": "9B", "allergies": "skaldjur", "external_account_id": "student_024"},
                {"name": "Ylva Tanaka", "grade": "10", "class": "10A", "allergies": "gluten, mjölk", "external_account_id": "student_025"}
    ]



def create_sample_meals() -> List[Dict[str, Any]]:
    return [
        {
            "name": "Köttbullar med potatismos",
            "description": "Klassiska svenska köttbullar serveras med krämigt potatismos och lingonsylt",
            "price": 120.00,
            "category": "Huvudrätt",
            "rating": 4.6,
            "rating_count": 30
        },
        {
            "name": "Stekt strömming med potatis",
            "description": "Stekt strömming med dillkokt potatis och skirat smör",
            "price": 135.00,
            "category": "Fiskrätt",
            "rating": 4.2,
            "rating_count": 18
        },
        {
            "name": "Vegetarisk lasagne",
            "description": "Lasagne med zucchini, aubergine och tomatsås, toppad med ost",
            "price": 125.00,
            "category": "Vegetariskt",
            "rating": 4.0,
            "rating_count": 22
        },
        {
            "name": "Korv Stroganoff",
            "description": "Klassisk korv stroganoff med ris",
            "price": 120.00,
            "category": "Huvudrätt",
            "rating": 3.9,
            "rating_count": 15
        },
        {
            "name": "Raggmunk med fläsk",
            "description": "Raggmunkar serveras med stekt fläsk och lingonsylt",
            "price": 140.00,
            "category": "Huvudrätt",
            "rating": 4.3,
            "rating_count": 20
        },
        {
            "name": "Fiskgratäng med dill",
            "description": "Fiskgratäng med dill och potatismos",
            "price": 130.00,
            "category": "Fiskrätt",
            "rating": 4.1,
            "rating_count": 17
        },
        {
            "name": "Grönsakssoppa med bröd",
            "description": "Värmande grönsakssoppa serveras med färskt bröd",
            "price": 120.00,
            "category": "Vegetariskt",
            "rating": 3.8,
            "rating_count": 12
        },
        {
            "name": "Pannkakor med sylt och grädde",
            "description": "Tunna pannkakor serveras med sylt och vispad grädde",
            "price": 125.00,
            "category": "Efterrätt",
            "rating": 4.7,
            "rating_count": 28
        }
    ]

def setup_database(db_path: str = 'test.db', reset: bool = False, verbose: bool = False) -> None:
    def log(message: str) -> None:
        if verbose:
            print(f"  {message}")
    
    print(f"Setting up database: {db_path}")
    
    if os.path.exists(db_path) and reset:
        os.remove(db_path)
    
    db = SchoolLunchDB(db_path)
    db.setup_initial_data()
    
    print("👥 Adding sample students...")
    students = create_sample_students()
    student_count = 0
    
    for student in students:
        try:
            db.add_student(student)
            student_count += 1
            log(f"Added student: {student['name']} (Grade {student.get('grade', 'N/A')}, Class {student.get('class', 'N/A')})")
        except Exception as e:
            print(f"⚠️  Error adding student {student['name']}: {e}")
    
    print(f"✅ Added {student_count} students")
    
    print("🍽️  Adding some serious gourmet shit")
    sample_meals = create_sample_meals()
    meal_count = 0
    
    existing_meals = db.get_all_meals()
    existing_count = len(existing_meals) if existing_meals else 0
    
    for meal in sample_meals:
        try:
            meal_id = db.add_meal(meal)
            
            if meal["rating_count"] > 0:
                target_rating = meal["rating"]
                rating_count = meal["rating_count"]
                
                for i in range(rating_count):
                    if i < rating_count // 2:
                        rating = min(5, target_rating + 0.5)
                    else:
                        rating = max(1, target_rating - 0.5)
                    db.rate_meal(meal_id, rating)
            
            meal_count += 1
            log(f"Added meal: {meal['name']} (${meal['price']:.2f}) - {meal['category']}")
            
        except Exception as e:
            print(f"⚠️  Error adding meal {meal['name']}: {e}")
    
    total_meals = existing_count + meal_count
    print(f"✅ Menu now has {total_meals} meals ({meal_count} added)")
    
    print("📊 Adding sample transaction data...")
    transaction_count = 0
    
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM students")
        student_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM meals")
        meal_ids = [row[0] for row in cursor.fetchall()]
        
        conn.close()
    except Exception as e:
        log(f"Error getting students/meals for transactions: {e}")
        student_ids = []
        meal_ids = []
    
    if student_ids and meal_ids:
        for days_ago in range(7):
            transaction_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            import random
            random.seed(42 + days_ago)
            
            for _ in range(random.randint(5, 15)):
                try:
                    student_id = random.choice(student_ids)
                    meal_id = random.choice(meal_ids)
                    
                    db.record_transaction(student_id, meal_id, transaction_date)
                    transaction_count += 1
                    
                except Exception as e:
                    log(f"Error adding transaction: {e}")
    
    print(f"✅ Added {transaction_count} sample transactions")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📋 DATABASE SETUP COMPLETE!")
    print("=" * 60)
    
    # Get final counts using direct SQL to avoid Row object issues
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM students")
        student_total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM meals")  
        meal_total = cursor.fetchone()[0]
        
        conn.close()
    except Exception as e:
        log(f"Error getting final counts: {e}")
        student_total = 0
        meal_total = 0
    
    print(f"👥 Total Students: {student_total}")
    print(f"🍽️  Total Meals: {meal_total}")
    print(f"📊 Sample Transactions: {transaction_count}")
    print(f"📁 Database File: {os.path.abspath(db_path)}")
    print(f"💾 Database Size: {os.path.getsize(db_path) / 1024:.1f} KB")
    
    print("\n🚀 Ready to launch! Run: python launch_application.py")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Setup school lunch database with sample data')
    parser.add_argument('--reset', action='store_true', help='Remove existing database')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--database', '-d', default='test.db', help='Database file path')
    
    args = parser.parse_args()
    
    try:
        success = setup_database(args.database, args.reset, args.verbose)
        print("\n✅ Setup completed!" if success else "\n❌ Setup failed.")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
