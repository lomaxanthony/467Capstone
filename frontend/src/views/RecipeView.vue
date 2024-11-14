<template>
    <div class="recipe-view">
        <h1>{{ user.name }}'s Recipes</h1>
        <ul>
            <li v-for="recipe in recipes" :key="recipe.id">
                <h2>{{ recipe.title }}</h2>
                <p>{{ recipe.description }}</p>
            </li>
        </ul>
    </div>
</template>

<script>

// Still need to figure out how to structure the data and what the API endpoint will be
export default {
    name: 'RecipeView',
    data() {
        
    },
    created() {
        this.fetchRecipes();
    },
    methods: {
        fetchRecipes() {
            // Fetch recipes from the API 
        }
    }
};
</script>

<style scoped>
.recipe-view {
    padding: 20px;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin-bottom: 20px;
}

h2 {
    font-size: 20px;
    margin: 0;
}

p {
    margin: 5px 0 0;
}
</style>