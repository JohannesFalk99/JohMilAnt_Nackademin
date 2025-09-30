"""
user.py - User class for login and registration
"""

from database import Database

class User:
    def __init__(self, user_id: int, username: str):
        self.id = user_id
        self.username = username

    @staticmethod
    def register(db: Database):
        username = input("Choose a username: ")
        password = input("Choose a password: ")

        conn = db.connect()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print("✅ User registered successfully!")
        except Exception as e:
            print("⚠️ Error registering user:", e)
        finally:
            conn.close()

    @staticmethod
    def login(db: Database):
        username = input("Username: ")
        password = input("Password: ")

        conn = db.connect()
        cur = conn.cursor()
        cur.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        conn.close()

        if row:
            print(f"✅ Welcome back, {row[1]}!")
            return User(row[0], row[1])
        else:
            print("❌ Invalid login.")
            return None
