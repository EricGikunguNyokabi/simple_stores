from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user

from app.models.products import Product
from app.models.users import User

main = Blueprint("main", __name__)

@main.route("/")
def home():
    try:
        products = Product.query.all() # Retrieve all products from the database
    except Exception as e: # Handle any exceptions that occur during the database query   
        products = []  # Fallback to an empty list if there's an error
        print(f"Error retrieving products: {e}")  # Log the error for debugging
    # Render the home template and pass the products to it
    return render_template("home.html", products=products)




@main.route("/home")
@login_required
def dashboard():
    try:
        products = Product.query.all() # Retrieve all products from the database
    except Exception as e: # Handle any exceptions that occur during the database query   
        products = []  # Fallback to an empty list if there's an error
        print(f"Error retrieving products: {e}")  # Log the error for debugging
    # Render the home template and pass the products to it
    return render_template("home.html", products=products)

