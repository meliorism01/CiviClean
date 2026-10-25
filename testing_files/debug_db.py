#!/usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

app = create_app()
print('Database URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
db_file = 'civiclean.db' if os.path.exists('civiclean.db') else ('instance/civiclean.db' if os.path.exists('instance/civiclean.db') else 'mapmywaste.db')
print('Database file path:', db_file)
print('File exists before:', os.path.exists(db_file))

with app.app_context():
    # Try to get the engine and inspect it
    from sqlalchemy import inspect
    
    inspector = inspect(db.engine)
    print('Tables found:', inspector.get_table_names())
    
    # Try manual create
    print('\nCalling db.create_all()...')
    db.create_all()
    
    print('File exists after:', os.path.exists(db_file))
    print('File size:', os.path.getsize(db_file) if os.path.exists(db_file) else 'N/A')
    
    # Re-inspect
    inspector = inspect(db.engine)
    print('Tables found after create_all:', inspector.get_table_names())
