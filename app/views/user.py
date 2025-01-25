from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from app import db
from app.forms.auth import RegistrationForm, LoginForm, RequestOtp, VerifyOtp,ResetPassword
from app.forms.user_profile import UserProfileForm
from app.models.users import User
from app.utils.otp import generate_otp

user = Blueprint("user",__name__,url_prefix="/user/")

mail = Mail()

@user.route("user-profile")
@login_required
def user_profile():
    form = UserProfileForm()
    return render_template("user/user_profile.html")


@user.route("verify-email")
@login_required
def verify_email():
    return redirect(url_for("user.user_profile"))


@user.route("verify-phone")
@login_required
def verify_phone():
    return redirect(url_for("user.user_profile"))


@user.route("edit-address")
@login_required
def edit_address():
    return redirect(url_for("user.user_profile"))
