from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)



class Favorites(db.Model):
    """Mapping user favorite recipes."""

    __tablename__ = 'favs' 

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.id', ondelete='cascade'),
        unique=True
    )


class User(db.Model):
    """User modeling."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )
    
    image_url = db.Column(
        db.Text,
        nullable=False,
        default = '/static/imgs/default-avatar.jpg'
    )


    favs = db.relationship(
        'Recipe',
        secondary="favs"
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"


    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Recipe(db.Model):
    """An Recipe Model"""

    __tablename__ = 'recipes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    name = db.Column(
        db.String(140),
        nullable=False,
    )

    searchID= db.Column(
        db.Integer,
        nullable=True,
        unique=True,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable = False,
        default = datetime.utcnow()
    )


    image_url = db.Column(
        db.Text,
        nullable=False,
        default='https://w7.pngwing.com/pngs/424/17/png-transparent-pierogi-kulich-roulade-cooking-recipe-cooking-purple-violet-recipe.png'
    )

    def __repr__(self):
        return f"<Recipe #{self.id}: {self.name}, {self.searchID}>"

    @classmethod
    def create(cls, name, searchID, image_url):
        """ Add recipe to database """

        recipe = Recipe(
            name=name,
            searchID=searchID,
            image_url=image_url,
        )

        db.session.add(recipe)
        recipe = recipe.query.filter_by(name=name).one()

        return recipe


  