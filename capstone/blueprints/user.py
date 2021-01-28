from flask import Blueprint, render_template, request, redirect, session, flash , url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from capstone.forms.editprofileform import EditProfile , ChangePasswordForm
from capstone.forms.additemform import AddItemForm
from capstone.models.user import User
from capstone.models.item import Item
from bson import ObjectId


# define our blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/user/edit_profile', methods=['POST', 'GET'])
def edit_profile_user():
    user = User.objects(id = session["user"]['id']).first()

    edit_profile_form = EditProfile()
    
    if request.method == "GET":

        edit_profile_form.new_first_name.data = session['user']['first_name']
        edit_profile_form.new_last_name.data = session['user']['last_name']
    
    if  edit_profile_form.validate_on_submit():

        new_first_name = edit_profile_form.new_first_name.data
        new_last_name = edit_profile_form.new_last_name.data
    
        user.first_name = new_first_name
        user.last_name = new_last_name
        

        user.save()

        session['user'] = user.serialize()

        return redirect(url_for('home.home')) 

    return render_template("profile/edit-profile.html", form = edit_profile_form)



@user_bp.route('/user/change_password', methods=['GET', 'POST'])
def change_password():

    user = User.objects(id=session['user']['id']).first()

    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():

        # read post values from the form
        current_password = change_password_form.current_password.data
        new_password = change_password_form.new_password.data

        if (user):
            user.change_password(current_password, new_password)
            user.save()
            flash("Your password has been successfully changed.")
            return redirect(url_for('user.change_password'))

    return render_template("profile/change-password.html", form=change_password_form)

@user_bp.route('/user/add_item', methods=['GET', 'POST'])
def add_item():

    add_item_form = AddItemForm()

    if add_item_form.validate_on_submit():

        title = add_item_form.title.data
        description = add_item_form.description.data
        price = add_item_form.price.data
        category = add_item_form.category.data

        new_item = Item(title = title, description = description, price = price, category = category)
        
        new_item.save()

        flash("Your item has been successfully added.")

        return redirect(url_for('home.home'))

    return render_template("item/add-item.html", form = add_item_form)