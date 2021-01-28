from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField 

# Log In Account Settings Forms
class LoginForm(FlaskForm):
    username = StringField("Username : ", [validators.InputRequired()], render_kw={"placeholder": "enter your username"})
    password = PasswordField("Password : ", [validators.InputRequired()] , render_kw={"placeholder": "enter your password"})
    submit = SubmitField("Log In")