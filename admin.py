from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
import os
from models import User, Recipe, Favorites, db

def getadmin(app):
    admin = Admin(app, name='W2E', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Recipe, db.session))
    admin.add_view(ModelView(Favorites, db.session))

def get_key():
    return "9973533"