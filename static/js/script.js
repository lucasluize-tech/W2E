// import {secret} from './k'

async function getRecipes(){
    /* this function will make a request to mealDB api
    and make a small list of random recipes*/
    
    // const request = await axios.get(`${secret.BASE_URL}/${secret.API_KEY}/latest.php`)
    const request = await axios.get(`https://www.themealdb.com/api/json/v2/9973533/latest.php`)
    const data = request.data

    for (let meal of data.meals){
        
        $('.recipes-example').append(
            `<div class="card-recipe" style="width: 18rem">\
                <img src="${ meal.strMealThumb }" class="card-img-top">\
                <div class="card-body">
                    <h5 class="card-title">${meal.strMeal}</h5>
                    <p><b>Category: </b>${meal.strCategory}</p>
            </div></div>`)
    }
    
}

getRecipes();