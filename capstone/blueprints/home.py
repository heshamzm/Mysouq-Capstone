from flask import Blueprint, render_template, request, redirect, session, flash , url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField
from capstone.forms import LoginForm
from capstone.models import user
from capstone.models.item import Item

# define our blueprint
home_bp = Blueprint('home', __name__)


@home_bp.route('/home', methods=['POST', 'GET'])
def home():

    items = Item.objects()

    return render_template('item/home.html', items = items)


@home_bp.route("/item/search", methods=['POST'])
def search_items():
    
    if request.method == 'POST':
        
        search_keyword = str(request.form['search_keyword'])  
        results = Item.objects.search_text(search_keyword).order_by('$text_score')
        
        return render_template("item/search-result.html" , items = results , search_keyword = search_keyword)