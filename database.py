import sqlite3
from typing import List, Dict, Optional

"""
SQL-kommandon som används i DatabaseHandler:

-- Skapa tabell
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    value TEXT,
    example_field TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Lägg till post
INSERT INTO records (name, value, example_field) VALUES (?, ?, ?);

-- Hämta post efter ID
SELECT * FROM records WHERE id = ?;

-- Hämta alla poster
SELECT * FROM records ORDER BY id;

-- Uppdatera post
UPDATE records SET name=?, value=?, example_field=?, updated_at=CURRENT_TIMESTAMP WHERE id=?;

-- Ta bort post
DELETE FROM records WHERE id=?;

-- Sök poster
SELECT * FROM records WHERE name LIKE ? OR value LIKE ? OR example_field LIKE ? ORDER BY id;

-- Räkna poster
SELECT COUNT(*) FROM records;
"""

class DatabaseHandler:
    """Enkel klass för att hantera databasen och poster."""

    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        """Skapar tabellen records om den inte redan finns."""
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value TEXT,
                example_field TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_record(self, data: Dict) -> int:
        """Lägg till en ny post och returnera dess ID."""
        cols, vals = zip(*data.items())
        placeholders = ','.join('?' * len(vals))
        query = f"INSERT INTO records ({','.join(cols)}) VALUES ({placeholders})"
        self.conn.execute(query, vals)
        self.conn.commit()
        return self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    def get_record(self, record_id: int) -> Optional[Dict]:
        """Hämta en post med specifikt ID."""
        row = self.conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
        return dict(row) if row else None

    def get_all_records(self) -> List[Dict]:
        """Hämta alla poster sorterade efter ID."""
        return [dict(r) for r in self.conn.execute("SELECT * FROM records ORDER BY id").fetchall()]

    def update_record(self, record_id: int, data: Dict) -> bool:
        """Uppdatera en post. Returnerar True om något ändrades."""
        if not data:
            return False
        set_clause = ', '.join(f"{k}=?" for k in data)
        values = list(data.values()) + [record_id]
        self.conn.execute(
            f"UPDATE records SET {set_clause}, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            values
        )
        self.conn.commit()
        return self.conn.total_changes > 0

    def delete_record(self, record_id: int) -> bool:
        """Ta bort en post."""
        self.conn.execute("DELETE FROM records WHERE id=?", (record_id,))
        self.conn.commit()
        return self.conn.total_changes > 0

    def search_records(self, term: str) -> List[Dict]:
        """Sök poster som innehåller sökordet i namn, värde eller exempel-fältet."""
        like_term = f"%{term}%"
        rows = self.conn.execute(
            "SELECT * FROM records WHERE name LIKE ? OR value LIKE ? OR example_field LIKE ? ORDER BY id",
            (like_term, like_term, like_term)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_record_count(self) -> int:
        """Räkna antal poster."""
        return self.conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]

    def close(self) -> None:
        """Stäng databasen."""
        self.conn.close()
