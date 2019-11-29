from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, IntegerField, StringField
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class RecipeForm(FlaskForm):
    title = StringField('Title')
    image = FileField('Image')
    preptime = IntegerField('Preparation')
    cooktime = IntegerField('Cooking')
    serves = IntegerField('Servings')
    source = StringField('Source')
    sourceurl = StringField('Source URL')
    notes = TextAreaField('Notes')
    type = SelectField('Type', choices=[
        ('main', 'Main'),
        ('starter', 'Starter'),
        ('dessert', 'Dessert'),
        ('bread', 'Bread'),
        ('snack', 'Snack'),
        ('drink', 'Drink')])
    vegetarian = BooleanField('Vegetarian', default=True)
    ingredients = TextAreaField('Ingredients')
    method = TextAreaField('Method')
    submit = SubmitField('Submit')
