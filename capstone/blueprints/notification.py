from flask import Blueprint, render_template, request, redirect, session, flash , url_for
from flask_wtf import FlaskForm
from capstone.models.user import User
from capstone.models.item import Item
from capstone.models.request import BuyRequest , UpgradeRequest
from capstone.blueprints.user import disable_user , login_required , maintenance
from bson import ObjectId

# define our blueprint
notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notification/review_buy_request', methods=['POST', 'GET'])
@login_required
@maintenance
@disable_user
def review_buy_request():

    current_user = User.objects(id = session['user']['id']).first()
    my_items = Item.objects(user = current_user)
    
    print(my_items)
    my_buy_requests = []
    for item in my_items:
            
        my_buy_requests.append(BuyRequest.objects(item = item))
 
    

    return render_template("notification/view-my-buy-request.html" , my_buy_requests = my_buy_requests)

@notification_bp.route('/notification/<item_id>/approve_buy_request/<request_id>', methods=['POST', 'GET'])
@login_required
@maintenance
@disable_user
def approve_buy_request(item_id,request_id ):
    """This function sets the "status" of a Buy Request to 'Approved'.
    Also, sets the "sold" attribute of the item to 'True'."""

    item = Item.objects(id = item_id).first()
    item.sold = True
    Item.objects(id = item_id).update_one(unset__buy_request_list = request_id)
    item.save()

    request = BuyRequest.objects(id = request_id).first()
    request.status = "Approved"
    request.save()

    flash("Item has been sold!")

    
    Item.objects(id = item_id).update_one(pull__buy_request_list = request_id)
    

    return redirect(url_for('notification.review_buy_request'))

@notification_bp.route('/notification/<item_id>/decline_request/<request_id>', methods=['POST', 'GET'])
@login_required
@maintenance
@disable_user
def decline_request(item_id,request_id):
    """This function sets the "status" of a Buy Request to 'Declined'."""

   
    Item.objects(id = item_id).update_one(unset__buy_request_list = request_id)

    request = BuyRequest.objects(id = request_id).first()
    request.status = "Declined"
    request.save()

    flash("Buy Request has been Declined!")
    
    return redirect(url_for('notification.review_buy_request'))


# upgrade requests functions



@notification_bp.route('/review_upgrade_requests', methods=['POST', 'GET'])
@login_required
@maintenance
@disable_user
def review_upgrade_requests():
    """This function is available for the Admin user to preview Upgrade Requests to choose to Approve or Decline."""

    users = User.objects()

    upgrade_requests = []

    for user in users:
        upgrade_requests.append(UpgradeRequest.objects(user = user).all())

    return render_template("notification/view-upgrades-requests.html", upgrade_requests = upgrade_requests)


@notification_bp.route('/approve_upgrade_request/<request_id>', methods=['POST', 'GET'])
@login_required
@maintenance
@disable_user
def approve_upgrade_request(request_id):
    """This function sets the "status" of an Upgrade Request to 'Approved'.
    Also, sets the "role" of the user to '1' (Seller)."""

    request = UpgradeRequest.objects(id = request_id).first()
    request.status = "Approved"
    request.save()

    request.user.role = 1
    request.user.save()
    
    flash("Upgrade Request has been approved.")

    return redirect(url_for("notification.review_upgrade_requests"))


@notification_bp.route('/decline_upgrade_request/<request_id>', methods=['POST', 'GET'])
@login_required
@maintenance
@disable_user
def decline_upgrade_request(request_id):
    """This function sets the "status" of an Upgrade Request to 'Declined'.
    Also, sets the "role" of the user to '0' (Buyer). Just in case the Admin changed their mind """

    request = UpgradeRequest.objects(id = request_id).first()
    request.status = "Declined"
    request.save()

    flash("Upgrade Request has been declined.")
    

    return redirect(url_for("notification.review_upgrade_requests"))