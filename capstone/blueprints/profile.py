from flask import Blueprint, render_template, request, redirect, session, flash , url_for
from flask_wtf import FlaskForm
from capstone.models.request import BuyRequest ,UpgradeRequest
from capstone.models.user import User
from capstone.models.item import Item , Category
from capstone.forms.items import AddCategoryForm
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
    
    items = Item.objects()
    seller_user = User.objects(role = 1)
    buyer_user = User.objects(role = 0)
    users = User.objects()

    return render_template('profile/display-users.html' , buyer_user = buyer_user , seller_user = seller_user , users = users , items = items)


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

@profile_bp.route('/unlock_disable_user/<user_id>', methods=['POST', 'GET'])
@login_required
@disable_user
@maintenance    
def unlock_disable_user_user_list(user_id) :
    
    user = User.objects(id = user_id).first()
    
    user.disable = False

    user.save()

    flash(f"Account '{user.username}' has been unlocked.!")


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
    
    items = []
    for i in range(0 ,len(favorite_items)):

        item = Item.objects(id = favorite_items[i]).first()
        items.append(item)
        print(items)
        
    
    return render_template("profile/user-favorite.html" , items = items)

@profile_bp.route('/disable_users_list', methods=['POST', 'GET'])
@login_required
@disable_user
@maintenance  
def disabled_list():

    users = User.objects(disable = True)

    return render_template('profile/blocked-list.html' , users = users, title = "Blocked-List" , icon = 'fas fa-users')
    

@profile_bp.route('/buy_request_list/<user_id>', methods=['POST', 'GET'])
@login_required
@disable_user
@maintenance 
def buy_request_list(user_id):


    list_request = BuyRequest.objects(user = session['user']['id'])

    return render_template('profile/buy-request-list.html'  , list_request = list_request)


@profile_bp.route('/request_upgrade', methods=['GET', 'POST'])
@login_required
@disable_user
@maintenance 
def request_upgrade():

    request = UpgradeRequest.objects(user = session['user']['id']).first()

    if not request:

        upgrade_request = UpgradeRequest(user = session['user']['id'], status = "Pending")

        upgrade_request.save()

    else:

        flash("You have already requested an upgrade.")

    return redirect(url_for('profile.profile'))


@profile_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
@disable_user
@maintenance
def add_category():

    add_category_form = AddCategoryForm()

    if add_category_form.validate_on_submit():


        category_value = add_category_form.value.data
        category_label = add_category_form.label.data

        new_category = Category( value = category_value, label = category_label)

        new_category.save()
        
        flash('New Category has been added.!')

        return redirect(url_for("profile.profile"))

    return render_template("profile/add-category.html", form = add_category_form)