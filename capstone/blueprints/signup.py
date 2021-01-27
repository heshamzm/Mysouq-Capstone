from flask import Blueprint, render_template, request, redirect, session, flash , url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from capstone.forms import SignUpForm
from capstone.models.user import User

# define our blueprint
signup_bp = Blueprint('signup', __name__)

@signup_bp.route("/signup" , methods = ['POST' , 'GET'])
def signup():

    # created an instance of our form
    signup_form = SignUpForm()

    # check if it is a form submission
    if signup_form.validate_on_submit():

        #create instance from user model
        user = User()
        
        # read values from the login wtform
        user.username = signup_form.username.data
        user.password = user.encrypt_password(signup_form.password.data)
        user.email = signup_form.email.data
        user.brithday = signup_form.birthday.data

        # save the user object
        user.save()

        return redirect(url_for("login.login"))

    return render_template("sign-up/sign-up.html" , form = signup_form) 