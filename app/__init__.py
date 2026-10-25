from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance and uploads directories exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path, 'instance'), exist_ok=True)
    
    # Normalize SQLite database URI to absolute path so SQLite never fails to create/open the db file
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri and db_uri.startswith('sqlite:///'):
        rel_path = db_uri[len('sqlite:///'):]
        if not os.path.isabs(rel_path):
            clean_rel = rel_path[len('instance/'):] if rel_path.startswith('instance/') else rel_path
            abs_db_path = os.path.abspath(os.path.join(app.instance_path, clean_rel))
            os.makedirs(os.path.dirname(abs_db_path), exist_ok=True)
            app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{abs_db_path}"
    
    upload_dir = os.path.join(app.root_path, '..', app.config.get('UPLOAD_FOLDER', 'uploads'))
    os.makedirs(upload_dir, exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    return app


# Default app instance for WSGI servers (e.g. gunicorn app:app)
app = create_app()
with app.app_context():
    try:
        db.create_all()
        from app.models import User
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@civiclean.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admin = User.query.filter(User.email.in_([admin_email, 'admin@civiclean.com', 'admin@mapmywaste.com'])).first()
        if not admin:
            admin = User(name='Admin', email=admin_email, role='admin', points=0)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user initialized: {admin_email}")
    except Exception as e:
        print(f"Database auto-init note: {e}")

