async function getRecipes(){
    /* this function will make a request to mealDB api
    and make a small list of random recipes*/

    
    const request = await axios.get(`/api/latest`)

    const data = request.data

    for (let meal of data.meals){
        
        $('.recipes-example').append(
            `<div class="card-recipe" style="width: 9rem">\
                <img src="${ meal.strMealThumb }" class="card-img-top">\
                <div class="card-body">
                    <a href="/recipe/${meal.idMeal}" class="card-title">${meal.strMeal}</a>
                    <p><b>Category: </b>${meal.strCategory}</p>
            </div></div>`)
    }
    
}


getRecipes();

