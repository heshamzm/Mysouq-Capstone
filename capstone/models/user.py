from mongoengine import *
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from bson import ObjectId

class User(Document):

    # define class metadata
    meta = {'collection' : 'user'}

    # define class fields
    username = StringField(required = True, unique= True)
    password = StringField(required = True)
    birthday = DateTimeField(required=True)
    firstname = StringField(required = True)
    lastname = StringField(required = True)
    email = EmailField(required=True)
    favorites = ListField(StringField())
    role = IntField(default = 0)
    disable = BooleanField(default = False)
    maintenance = BooleanField(default = False)

    # check the password validation
    def authenticate(self, username, password):
        # username / password -> from the login form
        # self.username / self.password -> from the database
        if username == self.username and pbkdf2_sha256.verify(password, self.password):
            return True
        else:
            return False

    # encrypt the password
    def encrypt_password(self, password):
        return pbkdf2_sha256.hash(password)
    
     # this method changes the user password
    def change_password(self, current_password, new_password):
        if pbkdf2_sha256.verify(current_password, self.password):
            self.password = self.encrypt_password(new_password)


    # this method serializes the object into a JSON object
    def serialize(self):
        serialized = {
            "id": str(self.pk),
            'username': self.username,
            'password': 'Cant help you bro :*',
            'firstname' : self.firstname,
            'lastname': self.lastname,
            'role': self.role,
            'email': self.email,
            'favorites': self.favorites,
            'disable': self.disable,
            'maintenance' : self.maintenance
        }

        return serialized        
