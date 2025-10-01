#!/usr/bin/env python3
"""
Quick status check of the school lunch system
"""

import sqlite3
import os
import requests

def system_status():
    """Check system status"""
    
    print("🏫 School Lunch System - Status Check")
    print("=" * 60)
    
    # Database check
    if os.path.exists('test.db'):
        try:
            conn = sqlite3.connect('test.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM students")
            student_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM meals")
            meal_count = cursor.fetchone()[0]
            
            print(f"✅ Database (test.db): {student_count} students, {meal_count} meals")
            
            conn.close()
        except Exception as e:
            print(f"❌ Database error: {e}")
    else:
        print("❌ Database (test.db) not found")
    
    # Web server check
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200:
            print("✅ Web server: Running on http://127.0.0.1:5000")
        else:
            print(f"⚠️  Web server: Responded with status {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Web server: Not accessible")
    
    print("\n📋 Quick Test Instructions:")
    print("1. Go to: http://127.0.0.1:5000")
    print("2. Enter username: Alice Johnson")
    print("3. Click Login (no password needed)")
    print("4. Test ordering and rating meals")

if __name__ == "__main__":
    system_status()
