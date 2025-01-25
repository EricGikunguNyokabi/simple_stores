# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # type: ignore
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_mail import Mail
from flask import current_app
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")  # Load configuration from Config class

    # session for app
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"  # Store session data on server
    Session(app)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)  # Set the duration for the remember cookie

    # Context Processor for global template variables
    @app.context_processor
    def inject_company_details():
        return {
            'company_name': app.config['COMPANY_NAME'],
            'company_email_1': app.config['COMPANY_EMAIL_1'],
            'company_email_2': app.config['COMPANY_EMAIL_2'],
            'company_phone_1': app.config['COMPANY_PHONE_1'],
            'company_phone_2': app.config['COMPANY_PHONE_2'],
            'company_url': app.config['COMPANY_URL']
        }

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = "auth.login"  

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.users import User
        return User.query.get(int(user_id))  # Load user by ID

    # Register blueprints
    from app.views import main 
    from app.views.admin import admin 
    from app.views.user import user
    from app.views.auth import auth 
    from app.views.cart import cart 
    from app.views.product import product

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(auth)
    app.register_blueprint(cart)
    app.register_blueprint(product)

    with app.app_context():
        db.create_all()

    return app