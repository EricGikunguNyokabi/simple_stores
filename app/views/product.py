from flask import Blueprint, render_template, redirect, url_for, request, flash,current_app
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from app import db
import os
# models
from app.models.products import Product
from app.models.users import User

product = Blueprint("product", __name__)

# display all products from the database
@product.route("/all_products", methods=["GET"])
@login_required
def all_products():
    products = Product.query.all()
    return render_template("products/all_products.html", products=products)



# SINGLE ITEM VIEW
@product.route("/product/<int:product_id>")
def single_product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    return render_template("products/single_product.html", product=product)

# Add new product into the database
@product.route("/add-product", methods=["POST", "GET"])
@login_required
def add_new_product():
    if request.method == "POST":
        try:
            product_name = request.form.get("product_name")
            product_category = request.form.get("product_category")
            price = request.form.get("price")
            description = request.form.get("description")
            product_image_path = request.files.get("product_image_path")

            # Validate required fields
            if not all([product_name, product_category, price, description, product_image_path]):
                flash("All fields are required, including an image!", "danger")
                return render_template("products/new_product.html", 
                                       product_name=product_name,
                                       product_category=product_category,
                                       price=price,
                                       description=description)

            # Validate numeric field
            try:
                product_cost = float(price)  # Corrected to use 'price'
            except ValueError:
                flash("Product cost must be a valid number.", "danger")
                return render_template("products/new_product.html", 
                                       product_name=product_name,
                                       product_category=product_category,
                                       price=price,
                                       description=description)

            # Secure file upload
            image_filename = secure_filename(product_image_path.filename)
            upload_folder = current_app.config["PRODUCT_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image_path.save(image_path)

            # Save product to the database using SQLAlchemy
            new_product = Product(
                product_category=product_category,
                product_name=product_name,
                description=description,
                price=product_cost,  # Use the validated product_cost
                product_image_path=f"/static/images/products/{image_filename}"  # Relative path for the database
            )
            db.session.add(new_product)
            db.session.commit()

            flash(f"Product '{product_name}' added successfully!", "success")
            return redirect(url_for("product.all_products"))
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("products/new_product.html", 
                                   product_name=product_name,
                                   product_category=product_category,
                                   price=price,
                                   description=description,
                                   error="Something went wrong")
    return render_template("products/new_product.html")




# View a single product
@product.route("/single_item/<int:product_id>")
def single_item(product_id):
    single_result = Product.query.get(product_id)  # Use the model to get the product
    if single_result is None:
        flash("Product not found.", "danger")
        return redirect(url_for("product.all_products"))
    return render_template("singleitem.html", single_item=single_result)



@product.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)  # Use get_or_404 to fetch the product
    print(f"\nEDIT IMAGE:  {product.product_image_path}")

    
    if request.method == "POST":
        # Form fields from the request
        product_name = request.form["product_name"]
        product_category = request.form["product_category"]
        description = request.form["description"]
        price = request.form["price"]  # Assuming you want to use "price" for cost
        product_image = request.files.get("product_image")  # Fetch the uploaded file if present

        # Update product details
        product.product_name = product_name
        product.product_category = product_category  # Keep the category name as is
        product.description = description
        product.price = price

        # Update the image if a new file is uploaded
        if product_image and product_image.filename:
            image_filename = secure_filename(product_image.filename)
            upload_folder = current_app.config["PRODUCT_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image.save(image_path)

            # Update the image path in the database
            product.product_image_path = f"/static/images/products/{image_filename}"

        # Commit updates to the database
        try:
            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for("product.all_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating the product: {str(e)}", "danger")

    # Render the form with pre-filled product details
    return render_template("products/edit_product.html", product=product)

# Delete a product
@product.route("/delete-product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)  # Use the model to get the product

    if product is None:
        flash("Product not found.", "danger")
        return redirect(url_for("product.all_products"))

    try:
        db.session.delete(product)  # Delete the product using the model
        db.session.commit()  # Commit the changes to the database
        flash("Product deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        flash(f"An error occurred while deleting the product: {str(e)}", "danger")

    return redirect(url_for("product.all_products"))