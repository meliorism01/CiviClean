from app import create_app, db
from app.models import User, Driver, Truck, Route, Assignment
app = create_app()
with app.app_context():
    db.create_all()
    # Create admin user if doesn't exist
    admin = User.query.filter(User.email.in_(['admin@civiclean.com', 'admin@mapmywaste.com'])).first()
    if not admin:
        admin = User(
            name='Admin',
            email='admin@civiclean.com',
            role='admin',
            points=0
        )
        admin.set_password('admin123')  # Change in production!
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: admin@civiclean.com / admin123")
    elif admin.email == 'admin@mapmywaste.com':
        admin.email = 'admin@civiclean.com'
        db.session.commit()
        print("Admin user updated: admin@civiclean.com / admin123")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
