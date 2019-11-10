import logging

from flask import Blueprint, request, abort
from flask_genshi import render_response

from ..model import Recipe

log = logging.getLogger(__name__)

recipes = Blueprint('recipes', __name__, template_folder='templates')

class IngredientGroup(list):
    title = ''

def ingredient_groups(text):
    group = IngredientGroup()
    groups = [group]
    for line in text.split('\n'):
        line = line.strip()
        if line.endswith(':'):
            group.title = line
        elif line:
            group.append(line)
        else:
            group = IngredientGroup()
            groups.append(group)
    return groups

@recipes.route('/')
def index():
    vegetarian = request.args.get('vegetarian')
    veg = bool(vegetarian)
    starters = Recipe.by_type('starter', vegetarian=veg)
    mains = Recipe.by_type('main', vegetarian=veg)
    desserts = Recipe.by_type('dessert', vegetarian=veg)
    snacks = Recipe.by_type('snack', vegetarian=veg)
    drinks = Recipe.by_type('drink', vegetarian=veg)
    breads = Recipe.by_type('bread', vegetarian=veg)
    mealsets = (
        ('Starters', starters),
        ('Main courses', mains),
        ('Desserts', desserts),
        ('Breads', breads),
        ('Snacks', snacks),
        ('Beverages', drinks),
    )
    authenticated = False
    # TODO - authentication
    # if identity.has_permission('recipe'):
    #    authenticated = True
    return render_response('recipes.html', dict(
        mealsets = mealsets,
        authenticated = authenticated,
        vegetarian = vegetarian,
    ))

@recipes.route('/<recipe_seo>')
def recipe(recipe_seo):
    recipe = Recipe.by_seo(recipe_seo)
    if not recipe:
        abort(404)
    return render_response('recipe.html', dict(
        title = recipe.title,
        notes = recipe.notes,
        prephours = recipe.preptime // 60,
        prepmins = recipe.preptime % 60,
        cookhours = recipe.cooktime // 60,
        cookmins = recipe.cooktime % 60,
        source = recipe.source,
        sourceurl = recipe.sourceurl,
        serves = recipe.serves,
        seo = recipe.seo,
        image = recipe.image or "/static/images/recipes/noimage.png",
        ingredients = ingredient_groups(recipe.ingredients),
        method = ingredient_groups(recipe.method),
        vegetarian = recipe.vegetarian,
        editable = False, # TODO - authentication
        id = recipe.id,
    ))


