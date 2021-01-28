from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators ,PasswordField ,TextAreaField
from wtforms.fields.html5 import EmailField , DateField

# Sign Up Account Settings Forms
class SignUpForm(FlaskForm):

    username = StringField("Username : ", [validators.InputRequired()] , render_kw={"placeholder": "enter your username"})
    password = PasswordField("Password : ", [validators.InputRequired()] , render_kw={"placeholder": "enter your password"})
    email = EmailField("Email : " , [validators.InputRequired()] , render_kw={"placeholder": "EX:mark@gample.com"})
    birthday = DateField("Brithday : " , [validators.InputRequired()] , format='%Y-%m-%d' , render_kw={"placeholder": "enter your day of birth"})
    submit = SubmitField("Sign-Up") 