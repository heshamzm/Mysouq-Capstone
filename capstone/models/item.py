from mongoengine import *
from datetime import datetime
from .user import User


# cirual error
# from . request import BuyRequest 


class Item(DynamicDocument):

    # define class metadata
    meta = {'collection' : 'Items',
             'indexes': [
                {'fields': ['$title', '$description'],
                 'default_language': 'english',
                 'weights': {'title': 10, 'description': 2}
                 }
            ]
            }

    # define class fields
    user = ReferenceField(User)
    title = StringField(required = True)
    description = StringField(required = True)
    date = DateTimeField(default = datetime.now())
    price = FloatField(required = True)
    sold = BooleanField(default = False)
    category = StringField(required = True)
    buy_request_list = ListField(StringField())
    hidden = BooleanField(default = False)

class Category(Document):

    meta = {'collection' : 'Categories'}

    value = StringField(required = True)
    label = StringField(required = True)


   