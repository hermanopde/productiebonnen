from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField, PasswordField
from wtforms.validators import InputRequired, data_required


class LoginForm(FlaskForm):
    email = EmailField(
        "Email")
    paswoord = PasswordField("paswoord", validators=[data_required()])
    submit = SubmitField("Log In")


class SearchField(FlaskForm):

    gezocht_order = StringField("InputOrder")
    submit_s = SubmitField("Zoek")


def optellen():
    print("optellen")
