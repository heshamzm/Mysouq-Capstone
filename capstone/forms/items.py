from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField, FloatField, SelectField, FileField


class AddItemForm(FlaskForm):

    title = StringField("Title: ", [validators.InputRequired()] , render_kw={"placeholder": "Like Car For Sale"})

    description = TextAreaField("Description: ", [validators.InputRequired()] , render_kw={"placeholder": "Like Toyota Camry model 2020 , Color-Black "})

    price = FloatField("Price: ", [validators.InputRequired()] , render_kw={"placeholder": "00.00 JDS"})

    category = SelectField(u'Category')

    image = FileField()

    submit = SubmitField("Add Item")


class EditItemForm(FlaskForm):

    title = StringField("Title: ", [validators.InputRequired()])
    description = TextAreaField("Description: ", [validators.InputRequired()])
    price = FloatField("Price: ", [validators.InputRequired()])
    category = SelectField(u'Category')
    submit = SubmitField("Edit Item")     


class AddCategoryForm(FlaskForm):
    value = StringField("Category Number: ")
    label = StringField("Category Name: ")
    submit = SubmitField("Add Category")