from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from app import db
from app.forms.user_profile import UserProfileForm
from app.models.users import User

user = Blueprint("user", __name__, url_prefix="/user/")

@user.route("user-profile", methods=["GET", "POST"])
@login_required
def user_profile():
    form = UserProfileForm()
    user = User.query.get(current_user.user_id)  # Get the current user

    if request.method == "POST" and form.validate_on_submit():
        # Update user profile logic here
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.user_profile"))

    # Populate form with current user data
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email

    return render_template("user/user_profile.html", form=form)

@user.route("verify-email")
@login_required
def verify_email():
    # Email verification logic here
    flash("Email verification link has been sent!", "info")
    return redirect(url_for("user.user_profile"))

@user.route("verify-phone")
@login_required
def verify_phone():
    # Phone verification logic here
    flash("Phone verification link has been sent!", "info")
    return redirect(url_for("user.user_profile"))

@user.route("edit-address")
@login_required
def edit_address():
    # Address editing logic here
    flash("Address updated successfully!", "success")
    return redirect(url_for("user.user_profile"))