import os
from flask import Flask
from mongoengine import *
import json
from capstone.models.user import User
from passlib.hash import pbkdf2_sha256
from capstone.models.item import Item , Category


def create_app(test_config=None):
    # create the Flask
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI="mongodb://root:example@localhost:27017/capstone?authSource=admin"
    )

    # connect to MongoDB using mongoengine
    connect(
        db='capstone',
        username='root',
        password='example',
        authentication_source='admin'
    )

    @app.route('/init-db')
    def init_db():
        
        common_password = pbkdf2_sha256.hash('1234')

        user_1 = User(username='Admin',password = common_password , birthday = "2009-12-30 14:09:01" , email = 'aaa@gmail.com', role = 2 , firstname='Admin', lastname='Admin').save()
        user_2 = User(username='hesham',password = common_password , birthday = "2009-12-30 14:09:01" , email = 'aaa@gmail.com', role = 0 , firstname='hesham', lastname='marei').save()
        user_3 = User(username='hamza',password = common_password , birthday = "2009-12-30 14:09:01" , email = 'aaa@gmail.com', role = 1 , firstname='hamza', lastname='radaideh').save()

        item_1 = Item(user = user_1 , title = "First", description = 'First' ,date = "2009-12-30 14:09:01", price = "0" , category = 'clothes').save()

        item_2 = Item(user = user_2 ,title = "Sec" , description = 'First' ,date = "2020-12-30 14:09:01", price = "0" , category = 'clothes').save()

        item_3 = Item(user = user_3 ,title = "Third", description = 'First' ,date = "2011-12-30 14:09:01", price = "0" , category = 'clothes').save()

        category_1 = Category(value = '1', label = 'Clothes').save()

        category_2 = Category(value = '2', label = 'Vehicles').save()
        
        category_3 = Category(value = '3', label = 'Digital Devices').save()

        return "Database initialized :)!"

    # register the blueprints
    from .blueprints.login import login_bp
    app.register_blueprint(login_bp)

    
    from .blueprints.signup import signup_bp
    app.register_blueprint(signup_bp)

    
    from .blueprints.home import home_bp
    app.register_blueprint(home_bp)

    from .blueprints.user import user_bp
    app.register_blueprint(user_bp)

    from .blueprints.profile import profile_bp
    app.register_blueprint(profile_bp)

    from .blueprints.notification import notification_bp
    app.register_blueprint(notification_bp)

    return app