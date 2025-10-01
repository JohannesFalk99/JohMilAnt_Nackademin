#!/usr/bin/env python3
"""
Simple login validation test
"""

import sqlite3
import os

def validate_login():
    """Show all valid login names from test.db"""
    
    if not os.path.exists('test.db'):
        print("❌ test.db not found!")
        return
    
    print("🔐 School Lunch System - Valid Login Names")
    print("=" * 60)
    
    try:
        # Connect directly to database
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, allergies FROM students ORDER BY name")
        students = cursor.fetchall()
        
        if students:
            print(f"📊 {len(students)} students can log in with their names:")
            print("-" * 60)
            
            for i, (student_id, name, allergies) in enumerate(students, 1):
                allergies_text = allergies if allergies and allergies != 'none' else "No allergies"
                print(f"{i:2d}. {name} (ID: {student_id})")
                print(f"     Allergies: {allergies_text}")
                print()
            
            print("💡 Login Instructions:")
            print("1. Go to: http://127.0.0.1:5000")
            print("2. Enter any student name as username (case doesn't matter)")
            print("3. Click 'Login' - no password needed!")
            print()
            print("🎯 Try these examples:")
            print(f"   • {students[0][1]}")  # First student
            print(f"   • {students[1][1]}")  # Second student
            print(f"   • {students[2][1]}")  # Third student
            
        else:
            print("❌ No students found!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    validate_login()
