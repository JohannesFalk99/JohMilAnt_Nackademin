#!/usr/bin/env python3
"""
Test login functionality with database users
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lunch_system_database import SchoolLunchDB

def test_login():
    """Test which usernames can be used for login"""
    
    print("🔐 School Lunch System - Login Test")
    print("=" * 60)
    
    # Initialize database
    db = SchoolLunchDB('test.db')
    
    # Get all students
    students = db.get_all_students()
    
    if not students:
        print("❌ No students found in database!")
        return
    
    print(f"📊 Found {len(students)} students who can log in:")
    print("-" * 60)
    
    for i, student in enumerate(students, 1):
        student_id = student[0]
        name = student[1]
        allergies = student[4] if len(student) > 4 and student[4] else "None"
        
        print(f"{i:2d}. Username: {name}")
        print(f"    ID: {student_id} | Allergies: {allergies}")
        print()
    
    print("💡 Login Instructions:")
    print("1. Go to http://127.0.0.1:5000")
    print("2. Enter any of the above names as username (case-insensitive)")
    print("3. No password required - just click Login")
    print()
    print("🎯 Example usernames to try:")
    print("   • Alice Johnson")
    print("   • alice johnson (case-insensitive)")
    print("   • Bob Smith")
    print("   • Carol Davis")

if __name__ == "__main__":
    test_login()
