from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    email = EmailField(
        "InputEmail", validators=InputRequired(message="nondedieu"))
    password = StringField("InputPassword", validators=InputRequired())
    submit = SubmitField("LogIn")
