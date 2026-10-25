import sqlite3, os

db = 'civiclean.db' if os.path.exists('civiclean.db') else ('instance/civiclean.db' if os.path.exists('instance/civiclean.db') else 'mapmywaste.db')
if not os.path.exists(db):
    print('DB not found', db)
else:
    con=sqlite3.connect(db)
    cur=con.cursor()
    cur.execute('PRAGMA table_info(waste_report);')
    rows=cur.fetchall()
    if not rows:
        print('Table waste_report not found')
    else:
        print('Columns in waste_report:')
        for r in rows:
            print('-', r[1])
    con.close()
