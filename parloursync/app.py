import os
from flask import Flask, redirect, url_for, render_template
from flask_login import current_user
from parloursync.config import Config
from parloursync.extensions import db, login_manager
from parloursync.routes.auth import auth_bp
from parloursync.routes.customer import customer_bp
from parloursync.routes.owner import owner_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(owner_bp)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'owner':
                return redirect(url_for('owner.dashboard'))
            return redirect(url_for('customer.dashboard'))
        return redirect(url_for('auth.login'))

    # Context processors to inject utilities if needed
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.now()}

    # Initialize database tables and seed initial data
    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from parloursync.models import User, Service, Staff
    
    # Check if we need to seed
    if User.query.count() == 0:
        # Create Owner
        owner = User(username='salon_owner', email='owner@parloursync.com', role='owner')
        owner.set_password('password')
        db.session.add(owner)

        # Create Customer
        customer = User(username='john_doe', email='customer@parloursync.com', role='customer')
        customer.set_password('password')
        db.session.add(customer)

    if Service.query.count() == 0:
        services = [
            Service(name='Signature Haircut', description='Precision cut tailored to your hair type, including a wash and blowout style.', price=45.0, duration_minutes=45),
            Service(name='Gel Manicure', description='Gel nail shaping, cuticle care, hand massage, and long-lasting gel polish.', price=35.0, duration_minutes=45),
            Service(name='Custom Facial', description='Deep pore cleansing, exfoliation, mask, and facial massage customized to your skin type.', price=75.0, duration_minutes=60),
            Service(name='Balayage & Styling', description='Hand-painted highlights for a natural, sun-kissed look, completed with hair styling.', price=150.0, duration_minutes=120)
        ]
        db.session.bulk_save_objects(services)

    if Staff.query.count() == 0:
        staff_members = [
            Staff(name='Sarah Jenkins', bio='Senior hair specialist with over 8 years of experience in custom cuts and styling.', email='sarah@parloursync.com'),
            Staff(name='Michael Chang', bio='Nail artist specializing in intricate nail art, gel extensions, and therapeutic hand care.', email='michael@parloursync.com'),
            Staff(name='Jessica Miller', bio='Licensed esthetician dedicated to clinical skincare treatments and organic facials.', email='jessica@parloursync.com')
        ]
        db.session.bulk_save_objects(staff_members)

    db.session.commit()


# Create the Flask app for Gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
