import sqlite3
import subprocess
import sys
from pathlib import Path


def test_fresh_database_setup(tmp_path):
    database = tmp_path / 'demo.db'
    subprocess.run(
        [sys.executable, 'create_sample_database.py', '--database', str(database)],
        cwd=Path(__file__).resolve().parents[2], check=True, capture_output=True,
    )
    with sqlite3.connect(database) as connection:
        assert connection.execute('SELECT COUNT(*) FROM students').fetchone()[0] == 25
        assert connection.execute('SELECT COUNT(*) FROM meals').fetchone()[0] == 8
        assert connection.execute('SELECT COUNT(*) FROM transactions').fetchone()[0] > 0
