#!/usr/bin/env python3
"""
Print all users from the school lunch database
"""

from lunch_system_database import SchoolLunchDB
import os

def print_all_users():
    """Print all users from the database"""
    
    # Check which database files exist
    databases = []
    if os.path.exists('test.db'):
        databases.append(('test.db', 'Test Database'))
    if os.path.exists('school_lunch.db'):
        databases.append(('school_lunch.db', 'Main Database'))
    if os.path.exists('school_food.db'):
        databases.append(('school_food.db', 'School Food Database'))
    
    if not databases:
        print("❌ No database files found!")
        return
    
    for db_file, db_name in databases:
        print(f"\n🗄️  {db_name} ({db_file})")
        print("=" * 60)
        
        try:
            db = SchoolLunchDB(db_file)
            
            # Get all students
            students = db.get_all_students()
            
            if not students:
                print("   No students found in this database.")
                continue
            
            print(f"   📊 Total Students: {len(students)}")
            print("   " + "-" * 55)
            
            # Print student details
            for i, student in enumerate(students, 1):
                # Convert Row object to dict or access by column name
                if hasattr(student, 'keys'):  # sqlite3.Row object
                    student_id = student['id'] if 'id' in student.keys() else student[0]
                    name = student['name'] if 'name' in student.keys() else student[1]
                    allergies = student['allergies'] if 'allergies' in student.keys() else (student[2] if len(student) > 2 else None)
                    external_id = student['external_account_id'] if 'external_account_id' in student.keys() else (student[3] if len(student) > 3 else None)
                    created_at = student['created_at'] if 'created_at' in student.keys() else (student[4] if len(student) > 4 else None)
                else:  # Regular tuple/list
                    student_id = student[0]
                    name = student[1]
                    allergies = student[2] if len(student) > 2 else None
                    external_id = student[3] if len(student) > 3 else None
                    created_at = student[4] if len(student) > 4 else None
                
                allergies = allergies if allergies else "None"
                external_id = external_id if external_id else "N/A"
                created_at = created_at if created_at else "N/A"
                
                print(f"   {i:2d}. {name}")
                print(f"       ID: {student_id} | Allergies: {allergies}")
                print(f"       External ID: {external_id}")
                if created_at != "N/A":
                    print(f"       Created: {created_at}")
                print()
                
        except Exception as e:
            print(f"   ❌ Error reading database: {e}")

    # Also check for hardcoded users in app.py
    print("\n🔧 Hardcoded Users in Flask App:")
    print("=" * 60)
    
    app_file = os.path.join('web_interface', 'flask_server.py')
    if os.path.exists(app_file):
        try:
            with open(app_file, 'r') as f:
                content = f.read()
                
            # Look for hardcoded users
            if 'test_users' in content:
                print("   Found hardcoded test users in app.py:")
                lines = content.split('\n')
                in_users_section = False
                for line in lines:
                    if 'test_users' in line and '{' in line:
                        in_users_section = True
                        print(f"   {line.strip()}")
                    elif in_users_section:
                        print(f"   {line.strip()}")
                        if '}' in line and line.strip().endswith('}'):
                            break
            else:
                print("   No hardcoded test users found in app.py")
                
        except Exception as e:
            print(f"   ❌ Error reading app.py: {e}")
    else:
        print("   ❌ app.py not found")

if __name__ == "__main__":
    print("👥 School Lunch System - All Users")
    print_all_users()
