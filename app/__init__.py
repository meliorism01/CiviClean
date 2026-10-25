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
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Create uploads and instance directories
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    upload_dir = os.path.join(app.root_path, '..', app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    
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

