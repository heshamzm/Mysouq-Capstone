from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators,PasswordField, TextAreaField  
from wtforms.validators import InputRequired, EqualTo, Length

# Log In Account Settings Forms
class EditProfile(FlaskForm):
    new_first_name = StringField("firstname : ", [validators.InputRequired()], render_kw={"placeholder": "enter new your firstname"})
    new_last_name = StringField("lastname : ", [validators.InputRequired()] , render_kw={"placeholder": "enter new your lastname"})
    submit = SubmitField("confirm Changes")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Enter your current password', [InputRequired()])
    new_password = PasswordField('Enter your new password', [InputRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField("Confirm your new password", [InputRequired()])
    submit = SubmitField("Change password")