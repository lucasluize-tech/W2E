// function to get all available categories from the api

async function getCategories() {
    const req = await axios.get('https://www.themealdb.com/api/json/v1/1/categories.php'
    )
    
    for (let cat of req.data.categories){
        $('#category').append(
            `<option value="${cat.strCategory}">${cat.strCategory}</option>`
            )
        }
}
    
// function to get all available Cuisine types from the api

async function getCuisine(){
    const req = await axios.get('https://www.themealdb.com/api/json/v1/1/list.php?a=list'
    )
    
    for (let cat of req.data.meals){
        $('#cuisine').append(
            `<option value="${cat.strArea}">${cat.strArea}</option>`
            )
        }
}
    
// function to get all available ingredients from the api

async function getIngredients(){
    const req = await axios.get('https://www.themealdb.com/api/json/v1/1/list.php?i=list'
    )
    
    for (let cat of req.data.meals){
        $('#ingredient').append(
            `<option value="${cat.strIngredient}">${cat.strIngredient}</option>`
            )
        }
    }
    
/* this function will make a request to mealDB api
and make a small list of latest recipes*/
async function getRecipes(){

    const request = await axios.get(`/api/random`)

    const data = request.data
    for (let i=6; i < data.meals.length; i++){
    // I just want the first four.
        const meal = data.meals[i];
        $('.latest-list').append(
            `<div class="card-recipe" style="width: 10rem;">\
                <img src="${ meal.strMealThumb }" class="card-img-top">\
                <div class="card-body">
                    <a href="/recipe/${meal.idMeal}" class="card-title">${meal.strMeal}</a>
                    <p><b>Category: </b>${meal.strCategory}</p>
            </div></div>`)
    }
}

// this function will render all matches by category
async function getMealByCategory(category) {
    req = await axios.get(`/api/category/${category}`)

        for (let meal of req.data.meals) {
            $('.results').append(
                `<li class="mb-2 item">
                    <img src="${meal.strMealThumb}" width="100px" height="100px" style="border-radius: 10px;">
                    <a class="recipe-link" href="/recipe/${meal.idMeal}">${meal.strMeal}</a>
                </li>`
            )
            
        }
}

// this function will render all matches by Cuisine
async function getMealByCuisine(cuisine) {
    req = await axios.get(`/api/category/${cuisine}`)

        for (let meal of req.data.meals) {
            $('.results').append(
                `<li class="mb-2 item">
                    <img src="${meal.strMealThumb}" width="100px" height="100px" style="border-radius: 10px;">
                    <a class="recipe-link" href="/recipe/${meal.idMeal}">${meal.strMeal}</a>
                </li>`
            )
            
        }
}

//this function will render all matches by Ingredient
async function getMealByIngredient(ingredient) {
    req = await axios.get(`/api/category/${ingredient}`)

        for (let meal of req.data.meals) {
            $('.results').append(
                `<li class="mb-2 item">
                    <img src="${meal.strMealThumb}" width="100px" height="100px" style="border-radius: 10px;">
                    <a class="recipe-link" href="/recipe/${meal.idMeal}">${meal.strMeal}</a>
                </li>`
            )
            
        }
}

//this function will render all matches by Meal name on the search form
async function getMealByName(mealName) {
    req = await axios.get(`/api/meal/${mealName}`)
        
        if (!req.data.meals) {
            $('.results').append(
                `<p class="mb-2 item">No matches found. Try again</p>`)
        }else {
            for (let meal of req.data.meals) {
                $('.results').append(
                    `<li class="item">
                        <a class="recipe-link" href="/recipe/${meal.idMeal}">
                            <img src="${meal.strMealThumb}" width="100px" height="100px" style="border-radius: 10px;">${meal.strMeal}</a>
                    </li>`
                )
            }
        }
}


// handle form requesting

$('.meal-form').on('submit', async function(e){
    e.preventDefault();
    $('.item').remove()

    const $categoryValue = $('#category').val()
    const $searchValue = $('#search').val()
    const $cuisineValue = $('#cuisine').val()
    const $ingredientValue = $('#ingredient').val()
    
    if ($categoryValue !== "none") {
        getMealByCategory($categoryValue)

    } else if ($cuisineValue !== "none") {
        getMealByCuisine($cuisineValue)

    }else if ($ingredientValue !== "none") {
        getMealByIngredient($ingredientValue)

    }else {
        getMealByName($searchValue)
    }
    // reset parameters after search

    $('.meal-form')[0].reset()
    $('.meal-form')[1].reset()
    $('.meal-form')[2].reset()
    $('.meal-form')[3].reset()
    
})

getRecipes();
getCategories();
getCuisine();
getIngredients();

