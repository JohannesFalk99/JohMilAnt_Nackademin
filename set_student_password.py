"""Set a password for an existing student without storing it in shell history."""
import argparse
import getpass
import os
from pathlib import Path
from lunch_system_database import SchoolLunchDB


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True, help='Full student name')
    parser.add_argument('--database', default=os.environ.get('DATABASE_PATH', 'test.db'))
    args = parser.parse_args()
    if not Path(args.database).is_file():
        parser.error('Database not found; create sample data first')
    db = SchoolLunchDB(args.database)
    try:
        students = db.db.execute('SELECT id FROM students WHERE LOWER(name) = LOWER(?)', (args.name,))
        if len(students) != 1:
            parser.error('Expected one matching student; check the name')
        password = getpass.getpass('New password (at least 12 characters): ')
        if password != getpass.getpass('Confirm password: '):
            parser.error('Passwords do not match')
        try:
            db.set_student_password(students[0]['id'], password)
        except ValueError as error:
            parser.error(str(error))
        print('Password updated.')
    finally:
        db.db.close()


if __name__ == '__main__':
    main()
