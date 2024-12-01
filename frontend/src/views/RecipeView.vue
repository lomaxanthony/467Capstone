<template>
    <div>
        <main>
            <!-- send recipes and groceries to Recipes component -->
            <Recipes :recipes="recipes" :groceries="groceries" />
        </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'; 
import Recipes from '@/components/Recipes.vue';

const recipes = ref([]);
const groceries = ref([]);
const user = ref(null);


// Fetch groceries for the specific user,
// then fetch recipes the recipe id for the food
// then fetch the recipe details
async function fetchGroceries() {
  try {
    console.log('Fetching groceries from backend'); // Debugging log
    const response = await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    
    // Explicitly set as an array because List component expects an array
    groceries.value = Array.isArray(data) ? data : [];
    
    console.log('Fetched groceries:', groceries.value); // Debugging log
    await fetchRecipeIds();
  } catch (error) {
    console.error('Failed to fetch groceries:', error);
  }
}

// Fetch recipe IDs for all groceries
async function fetchRecipeIds() {
  try {
    for (const grocery of groceries.value) {
      console.log('Fetching recipe id for:', grocery.name); // Debugging log
      const response = await fetch(`http://127.0.0.1:5000/api/${grocery.name}`);

      if (!response.ok) {
        throw new Error('Failed to get recipe id');
      }
      const data = await response.json();
      const recipeId = data[0].recipe_id;
      console.log('Fetched recipe id:', recipeId); // Debugging log

      // Fetch recipe details based on the recipe ID
      await fetchRecipeDetails(recipeId, grocery.name);
    }
  } catch (error) {
    console.error('Failed to fetch recipe ids:', error);
  }
}

// Fetch recipe details based on the recipe ID
async function fetchRecipeDetails(recipeId, foodName) {
  try {
    console.log('Fetching recipe details for recipe ID:', recipeId); // Debugging log
    const response = await fetch(`http://127.0.0.1:5000/api/${recipeId}`);

    if (!response.ok) {
      throw new Error('Failed to get recipe details');
    }
    const data = await response.json();
    console.log('Fetched recipe details:', data); // Debugging log

    // Add the recipe details to the recipes array
    recipes.value.push({recipe_name: data[0].recipe_name, recipe_url: data[0].recipe_url });
    console.log('Recipes:', recipes.value); // Debugging log
  } catch (error) {
    console.error('Failed to fetch recipe details:', error);
  }
}


onMounted(async function() {
  await fetchGroceries();
});
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
