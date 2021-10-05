import os
from unittest import TestCase
from models import db, User, Favorites, Recipe
from app import app

os.environ['DATABASE_URL'] = "postgresql:///W2E-test"

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):


    def setUp(self):

        User.query.delete()
        Favorites.query.delete()
        Recipe.query.delete()
        
        self.client = app.test_client()
        

    def test_user_model(self):

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.favs), 0)

    def test_recipe_model(self):

        r = Recipe(
            name="test@test.com",
            searchID="55555",
            image_url="x"
        )

        db.session.add(r)
        db.session.commit()

        self.assertEqual(r.searchID, 55555)

    
    def test_user_authenticate(self):

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.authenticate(u.email, u.password), u)
            
        self.assertFalse(User.authenticate('anyname', u.password))

        self.assertFalse(User.authenticate(u.username, 'pass'))