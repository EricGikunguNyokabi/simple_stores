from flask_wtf import FlaskForm
from wtforms import SubmitField

class UserProfileForm(FlaskForm):
    submit = SubmitField("UserPofile")
    