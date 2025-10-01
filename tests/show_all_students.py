#!/usr/bin/env python3
"""
Show all users from test.db database
"""

import sqlite3
import os

def show_database_users():
    """Show all users from test.db"""
    
    db_path = 'test.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    try:
        print(f"\n🗄️ Test Database ({db_path})")
        print("=" * 60)
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check what tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 Available tables: {[table[0] for table in tables]}")
        print()
        
        # Check if students table exists
        if any(table[0] == 'students' for table in tables):
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            print(f"📊 Total Students: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM students LIMIT 10")  # Show first 10
                students = cursor.fetchall()
                
                # Get column names
                cursor.execute("PRAGMA table_info(students)")
                columns = [col[1] for col in cursor.fetchall()]
                print(f"📋 Columns: {columns}")
                print("-" * 60)
                
                for i, student in enumerate(students, 1):
                    print(f"{i:2d}. Student Data:")
                    for j, column in enumerate(columns):
                        value = student[j] if j < len(student) else "N/A"
                        print(f"     {column}: {value}")
                    print()
                    
                if count > 10:
                    print(f"... and {count - 10} more students")
        else:
            print("❌ No 'students' table found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    print("👥 School Lunch System - User Display")
    show_database_users()
