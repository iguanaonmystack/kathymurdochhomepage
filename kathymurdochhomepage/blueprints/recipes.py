import logging

from flask import Blueprint, request, abort, redirect, flash, url_for
from flask_genshi import render_response
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..model import Recipe
from ..lib import helpers as h
from ..lib.recipes import RecipeForm

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
    vegetarian = request.args.get('vegetarian', 'yes')
    veg = vegetarian.lower() in h.true_strings
    starters = Recipe.by_type('starter', vegetarian=veg)
    mains = Recipe.by_type('main', vegetarian=veg)
    desserts = Recipe.by_type('dessert', vegetarian=veg)
    snacks = Recipe.by_type('snack', vegetarian=veg)
    drinks = Recipe.by_type('drink', vegetarian=veg)
    breads = Recipe.by_type('bread', vegetarian=veg)
    mealsets = (
        ('Starters', starters),
        ('Mains', mains),
        ('Desserts', desserts),
        ('Breads', breads),
        ('Snacks', snacks),
        ('Drinks', drinks),
    )
    authenticated = False
    # TODO - authentication
    # if identity.has_permission('recipe'):
    #    authenticated = True
    return render_response('recipes.html', dict(
        mealsets = mealsets,
        authenticated = authenticated,
        vegetarian = veg,
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
        editable = current_user.is_active,
        id = recipe.id,
    ))

@recipes.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    r = Recipe.get(request.values['id'])
    form = RecipeForm(obj=r)
    if form.validate_on_submit():
        r.set(
            title = form.title.data,
            notes = form.notes.data,
            preptime = int(form.preptime.data or 0),
            cooktime = int(form.cooktime.data or 0),
            source = form.source.data,
            sourceurl = form.sourceurl.data,
            serves = int(form.serves.data or 0),
            ingredients = form.ingredients.data,
            method = form.method.data,
            type = form.type.data,
            vegetarian = int(form.vegetarian.data))
        if form.image.data:
            form.image.data.save(r.image_disk)
        flash('Saved!')
        return redirect(url_for('.recipe', recipe_seo=r.seo))
    
    return render_response('edit_recipe.html', dict(
        id = r.id,
        form = form,
        image = r.image,
        # title = r.title,
        # notes = r.notes,
        # preptime = r.preptime,
        # cooktime = r.cooktime,
        # source = r.source,
        # sourceurl = r.sourceurl,
        # serves = r.serves,
        # ingredients = r.ingredients,
        # method = r.method,
        # type = r.type,
        # vegetarian = r.vegetarian,
        # mealtypes = form.type.choices,
    ))

