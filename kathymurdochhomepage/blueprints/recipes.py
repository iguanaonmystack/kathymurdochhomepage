import logging
import unicodedata

from flask import Blueprint, request, abort, redirect, flash, url_for
from flask_genshi import render_response
from flask_login import current_user, login_required

from ..model import Recipe
from ..lib import helpers as h
from ..lib.recipes import RecipeForm

log = logging.getLogger(__name__)

recipes = Blueprint('recipes', __name__, template_folder='templates')

class Ingredient:
    def __init__(self, text, scale):
        amount, orig_amt, text = self.process(text)
        self.scale = scale
        if scale == 1:
            self.amount = orig_amt
        elif amount is None:
            self.amount = None
        else:
            self.amount = round(amount * scale, 2)
            if self.amount == int(self.amount):
                self.amount = int(self.amount)
        self.original_amount = orig_amt
        self.text = text

    @classmethod
    def process(cls, text):
        val = 0
        integer = True
        for i, char in enumerate(text):
            if char.isdecimal():
                continue
            if i > 0 and char == '.':
                if not integer:
                    break
                integer = False
                continue
            break
        if i > 0:
            val = float(text[:i])
        # account for (probably mostly?) fractions after the number
        if len(text) > i:
            if text[i].isnumeric():
                numericvalue = unicodedata.numeric(text[i])
                val += numericvalue
                if integer:
                    integer = numericvalue == int(numericvalue)
                i += 1
        if integer:
            val = int(val)
        if i == 0:
            val = None
        return val, text[:i], text[i:].strip()

    def __str__(self):
        if self.scale == 1:
            return '{} {}'.format(self.original_amount, self.text)
        if self.amount:
            return '{} {}'.format(self.amount, self.text)
        return self.text

    def __repr__(self):
        return '<Ingredient {!r}, {!r}, {!r}, {!r}>'.format(
            self.amount, self.original_amount, self.scale, self.text)

class IngredientGroup(list):
    title = ''

def ingredient_groups(text, scale=None):
    group = IngredientGroup()
    groups = [group]
    for line in text.split('\n'):
        line = line.strip()
        if line.endswith(':'):
            group = IngredientGroup()
            groups.append(group)
            group.title = line
        elif line:
            if scale:
                group.append(Ingredient(line, scale))
            else:
                group.append(line)
        else:
            # blank line = new untitled set of ingredients
            group = IngredientGroup()
            groups.append(group)
    return filter(None, groups)

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
    scale_to = float(request.args.get('servings', recipe.serves))
    scale = 1
    if scale_to and recipe.serves:
        scale = scale_to / recipe.serves
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
        ingredients = ingredient_groups(recipe.ingredients, scale=scale),
        method = ingredient_groups(recipe.method),
        vegetarian = recipe.vegetarian,
        editable = current_user.is_active,
        id = recipe.id,
        scale = scale,
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
    ))

@recipes.route('/new', methods=('GET', 'POST'))
@login_required
def new():
    form = RecipeForm()
    if form.validate_on_submit():
        r = Recipe(
            title = form.title.data,
            seo = Recipe.make_seo(form.title.data),
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
        flash('Created!')
        return redirect(url_for('.recipe', recipe_seo=r.seo))
    return render_response('edit_recipe.html', dict(
        id = None,
        form = form,
        image = None,
    ))

@recipes.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    r = Recipe.get(request.values['id'])
    r.destroySelf()
    flash('Recipe deleted')
    return redirect(url_for('.index'))

