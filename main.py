"""
main.py - Entry point for the School Food App
"""

from database import Database
from user import User
from api_fetch import fetch_menu

def main():
    # Initialize database
    db = Database()
    db.create_tables()

    print("🍽️ Welcome apito the School Food App!")

    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Fetch Weekly Menu (API/JSON)")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            User.register(db)
        elif choice == "2":
            User.login(db)
        elif choice == "3":
            fetch_menu(db)
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
