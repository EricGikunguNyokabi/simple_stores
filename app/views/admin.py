from flask import Blueprint,Flask,render_template
from flask_login import login_user, login_required, logout_user, current_user


admin = Blueprint("admin",__name__,url_prefix="/admin/")


@admin.route("admin-dashboard")
@login_required
def admin_dash():
    return render_template("admin/admin_dashboard.html")