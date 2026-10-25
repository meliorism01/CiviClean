import sqlite3

import os
db_name = 'civiclean.db' if os.path.exists('civiclean.db') else ('instance/civiclean.db' if os.path.exists('instance/civiclean.db') else 'mapmywaste.db')
con = sqlite3.connect(db_name)
cur = con.cursor()
cur.execute("PRAGMA table_info(waste_report);")
rows = cur.fetchall()

print('Columns in waste_report table:')
for i, (cid, name, typ, notnull, dflt_value, pk) in enumerate(rows, 1):
    print(f"  {i}. {name:20} - {typ}")

con.close()
