from flask import Flask, render_template, redirect, request, session, flash, g
from models import connect_db, db, User, Recipe, Favorites
from forms import UserAddForm, UserEditForm, LoginForm
from flask_migrate import Migrate
import os, requests, re
# from admin import get_admin, get_key
from sqlalchemy.exc import IntegrityError, NoResultFound

CURR_USER_KEY = "curr_user"
API_URL = "https://www.themealdb.com/api/json/v2"
API_KEY = os.environ.get('API_KEY')

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
URI = os.environ.get('DATABASE_URL', 'postgresql:///W2E')
if URI.startswith("postgres://"):
    URI = URI.replace("postgres://", "postgresq://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "keepSecret")

# get_admin(app)

connect_db(app)
migrate = Migrate(app, db)

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/register', methods=["GET", "POST"])
def register():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/user/register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('/user/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('/user/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    if CURR_USER_KEY in session:
        session.pop(CURR_USER_KEY)
        flash("Successfully logged out!", category="danger")
        return redirect("/login")
    return redirect('/login')

##############################################################################
# Homepage and error pages

@app.route('/')
def homepage():
    """Show homepage:

    - anon users: Landing
    - logged in: Welcome screen + form + recipes list
    """
    
    if g.user:
  
        return render_template('home.html',
        user=g.user)

    else:
        return render_template('home-anon.html')


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

###############################
# User Routes:

@app.route('/users/favorites')
def favorites():
    """ Show list of favorites recipes """

    #make sure user is logged in
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    favorites = g.user.favs

    return render_template('/user/favorites.html', favorites=favorites)
    
@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    # make sure user is logged in
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    else:
        return render_template('user/profile.html', user=g.user)

@app.route('/users/edit', methods=["GET", "POST"])
def edit_user():
    """ edit user """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = UserEditForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(id=g.user.id).first()

        # if user's password is correct , edit.
        if User.authenticate(user.username, form.password.data):
            try:
                
                user.username = form.username.data if form.username.data else user.username
                user.email = form.email.data if form.email.data else user.email
                user.image_url = form.image_url.data if form.image_url.data else user.image_url
                
                db.session.add(user)
                db.session.commit()

                flash("Edited successfully!", 'success')
                return redirect('/users/profile')

            except IntegrityError:
                flash("E-mail already taken", 'danger')
                return render_template('user/edit.html', form=form, user=g.user)
        else:
            flash("Invalid Password", 'danger')
            return render_template('user/edit.html', form=form, user=g.user)
    else:
        return render_template('user/edit.html', form=form, user=g.user)


@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/login")

############################################################################
# Recipe route

@app.route('/recipe/<int:searchid>')
def recipe(searchid):
    """ this should return render page for the recipe """

    # check for logged user
    if not g.user:
        flash("Access unauthorized, login or register first!", "danger")
        return redirect("/")

    else:
        req = requests.get(f'{API_URL}/{API_KEY}/lookup.php?i={searchid}')

        data = req.json()
        data = data['meals'][0]

        ingredients = [data[key] for key in data if key.startswith('strIngredient') ]

        measurements = [data[key] for key in data if key.startswith('strMeasure') and data[key] != " "]

        if data['strTags']:
            tags = data.get('strTags').split(',')
        else:
            tags = []

        if data['strYoutube']:
            video = data.get('strYoutube').split('v=')[1]
        else: video=""
        try:
            recipe = Recipe.query.filter_by(searchID=searchid).one()
        except NoResultFound:
            recipe = None

        return render_template('recipe/recipe.html',
        name=data.get('strMeal'),
        image=data.get('strMealThumb'),
        ingredients=ingredients,
        measurements=measurements,
        tags=tags,
        instructions=data.get('strInstructions'),
        video=video,
        searchid=data.get('idMeal'),
        recipe=recipe,
        favs=g.user.favs
        )

@app.route('/favorites/add/<int:searchid>', methods=["POST"])
def add_favorite(searchid):
    ''' should add recipe to favorites list '''

    # check for logged user
    if not g.user:
        flash("You are not adding any recipe!", "danger")
        return redirect("/")

    req = requests.get(f'{API_URL}/{API_KEY}/lookup.php?i={searchid}')
    data = req.json()
    data = data['meals'][0]

    try:
        recipe = Recipe.query.filter_by(searchID=searchid).one()
    except NoResultFound:
        recipe = None

    if not recipe:
        recipe = Recipe.create(
            data.get('strMeal'),
            data.get('idMeal'),
            data.get('strMealThumb')
        )
        print(f'{g.user} added new recipe to db')
        

    add_fav = Favorites(user_id = g.user.id, recipe_id=recipe.id)
    db.session.add(add_fav)
    db.session.commit()

    flash('succesfully added to Favorites!', "success")
    return redirect(f"/recipe/{searchid}")

@app.route('/favorites/delete/<int:searchid>', methods=["POST"])
def delete_from_favorites(searchid):
    """ should delete from favorites """

    # check for logged user
    if not g.user:
        flash("You are not adding any recipe!", "danger")
        return redirect("/")

    recipe = Recipe.query.filter_by(searchID=searchid).first_or_404()
    Favorites.query.filter(Favorites.user_id == g.user.id, Favorites.recipe_id == recipe.id).delete()
    db.session.commit()

    flash("you removed from your favorites", "success")
    return redirect(f"/recipe/{searchid}")



############################################################################
# API 

@app.route('/api/latest')
def get_latest():
    """ this should return data for the latest recipes """

    res = requests.get(f'{API_URL}/{API_KEY}/latest.php')
    
    return res.json()

@app.route('/api/random')
def get_random():
    """ this should return data for random recipes """

    res = requests.get(f'{API_URL}/{API_KEY}/randomselection.php')
    
    return res.json()

@app.route('/api/category/<category>')
def get_list_by_category(category):
    """ this should return data for filtered recipes by category """

    res = requests.get(f'{API_URL}/{API_KEY}/filter.php', params={"c":category})

    return res.json()

@app.route('/api/cuisine/<cuisine>')
def get_list_by_cuisine(cuisine):
    """ this should return data for filtered recipes by cuisine """

    res = requests.get(f'{API_URL}/{API_KEY}/filter.php', params={"a":cuisine})

    return res.json()

@app.route('/api/ingredient/<ingredient>')
def get_list_by_ingredient(ingredient):
    """ this should return data for filtered recipes by ingredient """

    res = requests.get(f'{API_URL}/{API_KEY}/filter.php', params={"i":ingredient})

    return res.json()

@app.route('/api/meal/<meal>')
def get_list_by_meal(meal):
    """ this should return data for filtered recipes by meal name """

    meal= meal.strip().lower()
    res = requests.get(f'{API_URL}/{API_KEY}/search.php', params={"s":meal})

    return res.json()