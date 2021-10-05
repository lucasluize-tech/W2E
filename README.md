# What to Eat

A wrapper for the recipe [API](https://www.themealdb.com/api.php?=ref=apilist.fun)

Deployed App on heroku [here](https://w2e-project.herokuapp.com)

What to Eat is a Webapp to help users Find recipes by ingredients, cuisine, Categories and Meal name.

The user can also add recipes to a List of Favorites.
## Flow:

So User will Register/Login after seeing the landing Page with some of the latest Recipes and quick about.

After Register/login user will be able to quick search or get a list of random recipes.

User inside of a recipe page can add or remove to favorites , 
recipe page has Ingredients, Mesurements, Instructions and even a Embedded Youtube video of how to cook that meal.

### Technologies used for this project include:

- flask, flask-bcrypt, flask-wtforms, flask-sqlalchemy
- POSTGRESQL
- html, CSS, JS (Jquery, axios)

### working with this project locally:

Clone the repo, then after creating and activating a virtual environment:
```python
pip install -r requirements.txt
# don't forget to create a database for the app to connect.
createdb W2E
python seed.py #to create tables.

flask run  # to see the app running locally
```



