from flask import Blueprint,Flask,render_template,jsonify, session, redirect, url_for, request, flash
from flask_mail import Message
from app import db, mail
# models
from app.models.products import Product
from app.models.users import User
from app.models.order import Order, OrderItem



cart = Blueprint("cart",__name__,url_prefix="/cart")


@cart.route("/shopping-cart", methods=["GET", "POST"])
def shopping_cart():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "GET":
        # Fetch the cart items from session and calculate total price
        cart_items = session.get("cart", [])
        total_price = sum(item["price"] * item["quantity"] for item in cart_items)
        return render_template("cart/shopping_cart.html", cart_items=cart_items, total_price=total_price)

    if request.method == "POST" and request.is_json:
        data = request.get_json()
        product_id = data.get("product_id")
        action = data.get("action", "increment")

        # Ensure product_id exists in the request
        if not product_id:
            return jsonify({"success": False, "message": "Product ID is required."}), 400

        # If cart doesn't exist in the session, initialize it
        if "cart" not in session:
            session["cart"] = []

        cart = session["cart"]
        product = next((item for item in cart if item["product_id"] == product_id), None)

        if product:
            # If product found, perform the action based on increment/decrement
            if action == "increment":
                product["quantity"] += 1
            elif action == "decrement" and product["quantity"] > 1:
                product["quantity"] -= 1
            elif action == "decrement" and product["quantity"] == 1:
                cart.remove(product)
        else:
            # If product not found in the cart, attempt to fetch it from DB and add it to the cart
            db_product = Product.query.filter_by(product_id=product_id).first()
            if not db_product:
                return jsonify({"success": False, "message": "Product not found."}), 404

            cart.append({
                "product_id": db_product.product_id,
                "name": db_product.product_name,
                "price": db_product.price,
                "quantity": 1,
                "product_image_path": db_product.product_image_path,
            })

        session.modified = True

        # Recalculate the total price after the action
        total_price = sum(item["price"] * item["quantity"] for item in cart)
        cart_empty = len(cart) == 0

        return jsonify({
            "success": True,
            "updated_quantity": product["quantity"] if product else 1,
            "updated_item_total": product["price"] * product["quantity"] if product else 0,
            "new_total_price": total_price,
            "cart_empty": cart_empty,
        }), 200






@cart.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get("product_id")
        quantity = data.get("quantity", 1)

        if not product_id or quantity <= 0:
            return jsonify({"success": False, "message": "Invalid product ID or quantity."}), 400

        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return jsonify({"success": False, "message": "Product not found."}), 404

        # Add product to cart logic here...

        return jsonify({"success": True, "message": "Item added to cart."}), 200

    except Exception as e:
        print(f"Error adding to cart: {e}")
        return jsonify({"success": False, "message": "An error occurred while adding the item to the cart."}), 500



@cart.route("/cart-count", methods=["GET"])
def cart_count():
    # Calculate the total item count by summing the quantity of all items in the cart session
    total_items = sum(item["quantity"] for item in session.get("cart", []))
    
    # Print the total cart item count to the console (for debugging)
    print(f"total_items: {total_items}")
    
    # Return the count in JSON format for the AJAX call
    return jsonify({"count": total_items}), 200


# View for removing a product from the cart
@cart.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_items = session.get('cart', [])
    # Remove the product if it exists in the cart
    cart_items = [item for item in cart_items if item['product_id'] != product_id]
    session['cart'] = cart_items  # Update the session
    session.modified = True

    return redirect(url_for('cart.shopping_cart'))

# View for clearing the cart
@cart.route("/clear_cart", methods=["POST"])
def clear_cart():
    session.pop('cart', None)  # Clear the cart from session
    session.modified = True
    return redirect(url_for('cart.shopping_cart'))



# Route to display and place an order
@cart.route("/place-order", methods=["GET", "POST"])
def place_order():
    cart_items = session.get("cart", [])
    if not cart_items:
        return redirect(url_for("cart.shopping_cart"))

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    if request.method == "POST":
        return redirect(url_for("cart.finalize_order"))

    return render_template(
        "cart/place_order.html", cart_items=cart_items, total_price=total_price
    )



@cart.route("/finalize-order", methods=["GET", "POST"])
def finalize_order():
    # Retrieve order details
    shipping_address = request.form.get("shipping_address")
    contact_number = request.form.get("contact_number")
    cart_items = session.get("cart", [])
    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    # Redirect if essential details are missing
    if not shipping_address or not contact_number:
        flash("Missing required fields! Shipping address and contact number are mandatory.", "danger")
        return redirect(url_for("cart.place_order"))

    try:
        # Step 1: Save the main order record to the database
        order = Order(
            shipping_address=shipping_address,
            contact_number=contact_number,
            total_price=total_price
        )
        db.session.add(order)
        db.session.flush()  # Allows fetching 'order_id' without committing yet

        # Step 2: Save all cart items (order items) to the database
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item["product_id"],  # Corrected key
                product_name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
            )
            db.session.add(order_item)

        # Step 3: Commit all database changes
        db.session.commit()

        # Step 4: Prepare order confirmation details
        order_details = {
            "order_id": order.order_id,
            "shipping_address": shipping_address,
            "contact_number": contact_number,
            "cart_items": cart_items,
            "total_price": total_price,
        }

        # Step 5: Send confirmation email
        try:
            msg = Message(
                subject=f"Placed Order - #{order.order_id}",
                recipients=["wendybolo84@gmail.com"],  # Primary recipient
                bcc=["nyokabigikungueric@gmail.com"],  # Bcc recipient
                html=render_template("cart/order_success.html", order_details=order_details),
            )
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")  # Email failure shouldn't break order finalization

        # Step 6: Clear cart session after successful order
        session.pop("cart", None)

        # Step 7: Display success page with order details
        return render_template("cart/order_success.html", order_details=order_details)

    except Exception as e:
        db.session.rollback()  # Rollback in case of errors
        print(f"Error finalizing order: {e}")
        flash("An error occurred while finalizing the order. Please try again.", "danger")
        return redirect(url_for("cart.place_order"))