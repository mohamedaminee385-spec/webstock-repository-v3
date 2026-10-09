import os
import django

# Replace 'myproject' with your actual Django project folder name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webstock.settings")
django.setup()

import sqlite3

# Build an absolute path to ensure you connect to the existing db.sqlite3 file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auth_group")
    rows = cursor.fetchall()

for row in rows:
    print(row)




with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

print("Tables found in database:")
for t in tables:
    print(f"- {t}")