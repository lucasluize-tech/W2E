import os
from unittest import TestCase
from models import db, connect_db, Favorites, User, Recipe
from app import app, CURR_USER_KEY

os.environ['DATABASE_URL'] = "postgresql:///W2E-test"

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views """

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Favorites.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.recipe = Recipe.create(name="Ceviche",
        searchID="52773", image_url='https://w7.pngwing.com/pngs/424/17png-transparent-pierogi-kulich-roulade-cooking-recipe-cooking-purple-violet-recipe.png')

        self.user_favorite = Favorites(userid=self.testuser.id, recipe_id=self.recipe.id)

        db.session.commit()

    def test_user_page(self):
        

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(resp.data)

    def test_user_favorites(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/users/favorites")
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(resp.data)