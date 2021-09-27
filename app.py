from flask import Flask, render_template, redirect, request, session, flash, g
from models import connect_db, db, User, Recipe, Favorites
from forms import UserAddForm, UserEditForm, LoginForm
from flask_migrate import Migrate
import os
from flask_admin import Admin


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

admin = Admin(app, name='W2E', template_mode='bootstrap3')

connect_db(app)
migrate = Migrate(app, db)

@app.route('/')
def landing():
    '''should render the landing page'''
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('index.html', form=form)