from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    product_image_path = db.Column(db.String(255), nullable=True)

    sku = db.Column(db.String(50), unique=True, nullable=True)  # Stock Keeping Unit
    stock_quantity = db.Column(db.Integer, default=0, nullable=True)  # Available stock
    is_active = db.Column(db.Boolean, default=True)  # Product availability

    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Update timestamp
    
    brand = db.Column(db.String(100), nullable=True)  # Brand name
    tags = db.Column(db.Text, nullable=True)  # Tags for searchability
    discount_price = db.Column(db.Float, nullable=True)  # Discounted price

    def __repr__(self):
        return f'<Product {self.product_name}>'