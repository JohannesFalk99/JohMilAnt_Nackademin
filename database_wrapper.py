import sqlite3
import threading

# Klass SQLite-databas
class SQLiteDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self._local = threading.local()
    
    # Skapa eller hämta databasanslutning för aktuell tråd
    def _get_connection(self):
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    # Kör SELECT-frågor och returnera resultat
    def execute(self, sql, params=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchall()
    
    # Kör INSERT/UPDATE/DELETE och returnera rad-ID
    def execute_write(self, sql, params=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        conn.commit()
        return cursor.lastrowid
    
    def transaction(self):
        return self
    
    # Transaktionshantering med context manager
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        conn = self._get_connection()
        if exc_type is None:
            conn.commit()
        else:
            conn.rollback()
    
    # Stäng databasanslutning
    def close(self):
        if hasattr(self._local, 'conn'):
            self._local.conn.close()
