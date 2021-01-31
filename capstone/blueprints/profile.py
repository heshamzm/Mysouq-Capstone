from flask import Blueprint, render_template, request, redirect, session, flash , url_for
from flask_wtf import FlaskForm
from capstone.models.user import User
from capstone.models.item import Item
from bson.objectid import ObjectId
from .user import disable_user , login_required , maintenance

profile_bp = Blueprint('profile', __name__)


@profile_bp.route("/" , methods = ['POST' , 'GET'])
@profile_bp.route('/profile', methods=['POST', 'GET'])
@maintenance
@login_required
@disable_user
def profile():

    user = User.objects(id = session["user"]['id']).first()

    return render_template('profile/profile.html' , user = user)

@profile_bp.route('/display-users', methods=['POST', 'GET'])
@maintenance
@login_required
@disable_user
def display_users():

    users = User.objects()

    return render_template('profile/display-users.html' , users = users)


@profile_bp.route('/remove_user/<user_id>', methods=['POST', 'GET'])
@maintenance
@login_required
@disable_user
def remove_user(user_id):

    User.objects(id = user_id).first().delete()

    return redirect(url_for('profile.display_users'))

@profile_bp.route('/disable_user/<user_id>', methods=['POST', 'GET'])
@maintenance
@login_required
@disable_user    
def disable_user_list(user_id) :
    
    user = User.objects(id = user_id).first()
    
    user.disable = True

    user.save()

    return redirect(url_for('profile.display_users'))

@profile_bp.route('/profile/maintenance', methods=['POST', 'GET'])
@maintenance
@login_required
@disable_user    
def maintenance_mode() :

    User.objects(role = 0 and 1).update(maintenance = True) 
    
    return redirect(url_for('profile.profile'))


@profile_bp.route('/profile/remove_maintenance_mode', methods=['POST', 'GET'])
@maintenance
@login_required
@disable_user    
def remove_maintenance_mode() :
    
    User.objects(role = 0 and 1).update(maintenance = False) 
    
    return redirect(url_for('profile.profile'))

@profile_bp.route('/user/favorite_list', methods=['GET', 'POST'])
@maintenance
@login_required
@disable_user
def view_favorite():

    favorite_items = User.objects(id = session['user']['id']).get().favorites
    items = Item.objects(Objectid = favorite_items)
    # print(favorite_items)

    return render_template("profile/user-favorite.html" , items = items)