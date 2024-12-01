<template>
    <div class="recipe-list">
      <h1>Groceries and Recipes</h1>
      <div class="grid-container" v-if="groceries.length && recipes.length">
        <div v-for="(grocery, index) in groceries" :key="grocery.id" class="grid-item">
          <div class="grocery-item">
            <span class="grocery-name">{{ grocery.name }} 
                (
                <span class="grocery-quantity"> {{ grocery.quantity }}</span>
                )
            </span>
            
          </div>
          <div class="recipe-item" v-if="recipes[index]">
            <span class="recipe-name">{{ recipes[index].recipe_name }}</span>
            <button class="recipe-button">
              <a :href="recipes[index].recipe_url" target="_blank" class="recipe-url">View Recipe</a>
            </button>
          </div>
        </div>
      </div>
      <p v-else>No groceries or recipes found</p>
    </div>
  </template>
   
<script setup>
   import { defineProps, computed } from 'vue';
   
   const props = defineProps({
     groceries: {
       type: Array,
       default: () => []
     },
     recipes: {
       type: Array,
       default: () => []
     }
   });
</script>

<style scoped>
.recipe-list {
  padding: 20px;
}

h1 {
  color: var(--freshVeg);
  font-size: 34px;  
  margin-bottom: 20px;
  text-align: center;
}

.recipe-name {
  font-size: 20px;
  color:var(--flagRed);
  font-weight: bold;
  margin-bottom: 10px;
  display: block;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.grid-item {
  background-color: var(--glacierWater);
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.grocery-item {
  font-weight: bold;
  margin-bottom: 10px;
}

.recipe-item {
  margin-top: 10px;
  color: #666;
}

.recipe-button {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 15px;
  background-color: var(--lighterMountainShadow);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.recipe-button a {
  color: white;
  text-decoration: none;
}

.recipe-button:hover {
  background-color: var(--leafyGreen);
}

.recipe-url {
  color: white;
  text-decoration: none;
}

.recipe-url:hover {
  text-decoration: underline;
}
</style>