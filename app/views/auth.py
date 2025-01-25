from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from app import db
from app.forms.auth import RegistrationForm, LoginForm, RequestOtp, VerifyOtp,ResetPassword
from app.models.users import User
from app.utils.otp import generate_otp

auth = Blueprint("auth",__name__,url_prefix="/auth/")

mail = Mail()


@auth.route("register", methods=["POST","GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        phone = form.phone.data
        password = form.password.data
        # chech if the user already exists using email and phone
        existing_user = User.query.filter((User.email == email) | (User.phone == phone )).first()
        if existing_user:
            flash("Email or password already exists","danger")
            return redirect(url_for("auth.register"))
        # els create a new user
        new_user = User(
            email = email,
            phone = phone,
            password_hash = generate_password_hash(password)
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"An error:  {e} occured", "danger")
            return redirect(url_for("auth.register"))
    return render_template("auth/register.html",form=form)



@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    print(f"Request method: {request.method}")
    print(f"Form data: {form.data}")
    print(f"Form validation errors: {form.errors}")

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        print(f"Database user: {user}")
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=form.remember_me.data)
            flash("Login Successful", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)






@auth.route("forgot-password", methods=["POST", "GET"])
def forgot_password():
    form = RequestOtp()
    if form.validate_on_submit():
        email = form.email.data

        user = User.query.filter_by(email=email).first()
        if user:
            otp = generate_otp()  # Call the external generate_otp function
            user.otp = otp  # Set the OTP on the user object
            user.otp_created_at = datetime.now()  # Set the creation time
            db.session.commit()  # Save changes to the database
            
            msg = Message(
                "Your OTP Code",
                sender="WENDY-OTP",
                recipients=[email]
            )
            msg.body = f"Your OTP code is: {otp}"  # Include the OTP in the email body
            mail.send(msg)  # Send the email
            flash(f"An OTP has been sent to email address: {email}", "success")
            return redirect(url_for("auth.verify_otp", email=email))
        else:
            flash("Email address not found.", "danger")
    return render_template("auth/forgot_password.html", form=form)








@auth.route("verify-otp", methods=["POST", "GET"])
def verify_otp():
    form = VerifyOtp()
    email = request.args.get("email")  # Retrieve email from query parameter
    
    if request.method == "POST" and form.validate_on_submit():
        otp_input = form.otp.data  # Get the OTP entered by the user
        user = User.query.filter_by(email=email).first()  # Retrieve the user by email

        if not user:
            flash("Invalid email address. Please request a new OTP.", "danger")
            return redirect(url_for("auth.forgot_password"))

        if user.otp != otp_input:
            flash("Invalid OTP. Please try again.", "danger")
            return redirect(url_for("auth.verify_otp", email=email))

        # Ensure the OTP is still valid (e.g., expires in 30 minutes)
        if user.otp_created_at and datetime.now() - user.otp_created_at > timedelta(minutes=30):
            flash("The OTP has expired. Please request a new one.", "danger")
            return redirect(url_for("auth.forgot_password"))

        # OTP is valid - clear it from the database for security
        user.otp = None
        user.otp_created_at = None
        db.session.commit()

        flash("OTP verified successfully. You can now reset your password.", "success")
        return redirect(url_for("auth.reset_password", email=email))

    return render_template("auth/verify_otp.html", form=form, email=email)  # Pass email to the template


@auth.route("reset-password", methods=["POST", "GET"])
def reset_password():
    form = ResetPassword() # Ensure you are using the correct form class
    email = request.args.get("email")  # Retrieve email from query parameter

    if request.method == "POST" and form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email address. Please request a new OTP.", "danger")
            return redirect(url_for("auth.forgot_password"))

        # Update the user's password
        user.password_hash = generate_password_hash(password)  # Hash the new password
        db.session.commit()  # Commit the changes to the database

        flash("Your password has been reset successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html", form=form, email=email)  # Pass email to the template



@auth.route("/logout")
def logout():
    logout_user()  # Log the user out
    flash("You have been logged out.", "success")  # Optional: Flash a message
    return redirect(url_for("main.home"))  # Redirect to the home page or another page