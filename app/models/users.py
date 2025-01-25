from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    wishlist = db.Column(db.Text, nullable=True)
    account_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    otp = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow )
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User  {self.email}>'
    
    # Flask-Login requires these properties
    @property
    def is_active(self):
        return True  # You can implement your own logic here

    @property
    def is_authenticated(self):
        return True  # Always return True for authenticated users

    @property
    def is_anonymous(self):
        return False  # Always return False for authenticated users

    def get_id(self):
        return str(self.user_id)  # Return the user ID as a string
    
    # the __repr__ method in Python is a special method used to define how an object is represented as a string, primarily for debugging and development purposes.

    

    