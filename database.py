"""
database.py - Handles SQLite database connection and tables
"""

import sqlite3

class Database:
    def __init__(self, db_name: str = "school_food.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """
        Create tables: users, meals, ratings
        """
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            day TEXT,
            type TEXT,
            allergens TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            meal_id INTEGER,
            rating INTEGER,
            comment TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(meal_id) REFERENCES meals(id)
        )
        """)

        conn.commit()
        conn.close()
