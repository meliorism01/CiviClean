import sqlite3

import os
db_name = 'civiclean.db' if os.path.exists('civiclean.db') else ('instance/civiclean.db' if os.path.exists('instance/civiclean.db') else 'mapmywaste.db')
con = sqlite3.connect(db_name)
cur = con.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)

if tables:
    for table in tables:
        cur.execute(f"PRAGMA table_info({table});")
        cols = [r[1] for r in cur.fetchall()]
        print(f"  {table}: {cols}")

con.close()
