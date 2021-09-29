from flask import Flask, render_template, redirect, request, session, flash, g
from models import connect_db, db, User, Recipe, Favorites
from forms import UserAddForm, UserEditForm, LoginForm
from flask_migrate import Migrate
import os
from admin import getadmin
from sqlalchemy.exc import IntegrityError


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///W2E'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'darkly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

getadmin(app)

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

@app.route('/signup', methods=["GET", "POST"])
def signup():
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
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


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
        recipe_ids = []
        for recipe in g.user.recipes:
            recipe_ids.append(recipe.searchID)

        recipes= (Recipe
                    .query
                    .filter(Recipe.user_id.in_(recipe_ids))
                    .limit(3)
                    .all())
        
        
        return render_template('home.html', recipes=recipes, 
        favs=g.user.favs)

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
    
    favorites = Favorites.query.filter_by(user_id=g.user.id).all()

    return render_template('favorites.html', favorites = favorites)
    
@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    # make sure user is logged in
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
                flash("Username already taken", 'danger')
                return render_template('users/edit.html', form=form, user=g.user)
        else:
            flash("Invalid Password", 'danger')
            return render_template('users/edit.html', form=form, user=g.user)
    else:
        return render_template('users/edit.html', form=form, user=g.user)

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

