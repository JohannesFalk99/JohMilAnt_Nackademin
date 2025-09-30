"""
api_fetch.py - Fetch weekly menu from JSON or API
"""

import json
from database import Database

def fetch_menu(db: Database):
    """
    Loads meals from menu.json and stores them in database.
    If meals already exist for that day, skip them.
    """
    try:
        with open("menu.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("❌ menu.json not found! Please add the file.")
        return
    except json.JSONDecodeError:
        print("❌ Error reading menu.json (invalid JSON).")
        return

    meals = data.get("meals", [])
    if not meals:
        print("⚠️ No meals found in menu.json")
        return

    conn = db.connect()
    cur = conn.cursor()

    added = 0
    skipped = 0

    for meal in meals:
        cur.execute("""
        SELECT id FROM meals WHERE name=? AND day=? AND type=?
        """, (meal["name"], meal["day"], meal["type"]))
        exists = cur.fetchone()

        if exists:
            skipped += 1
        else:
            cur.execute("""
            INSERT INTO meals (name, day, type, allergens)
            VALUES (?, ?, ?, ?)
            """, (meal["name"], meal["day"], meal["type"], meal["allergens"]))
            added += 1

    conn.commit()
    conn.close()

    print(f"✅ {added} meals added, ⚠️ {skipped} duplicates skipped.")
