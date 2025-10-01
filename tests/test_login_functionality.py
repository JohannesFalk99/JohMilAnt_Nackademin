#!/usr/bin/env python3
"""
Test the login functionality directly
"""

import sqlite3
import os

def test_database_login():
    """Test login logic against test.db"""
    
    if not os.path.exists('test.db'):
        print("❌ test.db not found!")
        return
    
    print("🔧 Testing Database Login Logic")
    print("=" * 50)
    
    # Test username
    test_username = "Alice Johnson"
    
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        # Same query as in the Flask app
        cursor.execute("SELECT id, name FROM students WHERE LOWER(name) = LOWER(?)", (test_username,))
        student = cursor.fetchone()
        
        conn.close()
        
        if student:
            print(f"✅ Login SUCCESS for '{test_username}'")
            print(f"   Student ID: {student[0]}")
            print(f"   Name: {student[1]}")
        else:
            print(f"❌ Login FAILED for '{test_username}'")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Test case variations
    print("\n🧪 Testing Case Variations:")
    test_names = ["alice johnson", "ALICE JOHNSON", "Alice johnson", "bob smith", "CAROL DAVIS"]
    
    for name in test_names:
        try:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM students WHERE LOWER(name) = LOWER(?)", (name,))
            student = cursor.fetchone()
            conn.close()
            
            if student:
                print(f"   ✅ '{name}' → Found: {student[1]}")
            else:
                print(f"   ❌ '{name}' → Not found")
                
        except Exception as e:
            print(f"   ❌ '{name}' → Error: {e}")

if __name__ == "__main__":
    test_database_login()
