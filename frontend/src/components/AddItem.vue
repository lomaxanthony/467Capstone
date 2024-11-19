<template>
  <div class="form-container">
    <h2>Add Item</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="food_name">Food Name</label>
        <input id="food_name" v-model="newItem.food_name" placeholder="e.g., tomatoes" required />
      </div>
      <div class="form-group">
        <label for="expiration_days">Expiration Days</label>
        <input id="expiration_days" v-model.number="newItem.expiration_days" type="number" placeholder="Expiration Days" required />
      </div>
      <div class="form-group">
        <label for="food_type">Food Type</label>
        <select id="food_type" v-model="newItem.food_type" required>
          <option value="" disabled>Select food type</option>
          <option value="Meat">Meat</option>
          <option value="Produce">Produce</option>
          <option value="Dairy">Dairy</option>
          <option value="Grains">Grains</option>
          <option value="Snacks">Snacks</option>
          <option value="Breads">Breads</option>
        </select>
      </div>
      <div class="form-actions">
        <button type="submit" class="btn btn-primary">Add Item</button>
        <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['item-added', 'close']);
const newItem = ref({ food_name: '', expiration_days: 0, food_type: '' });

const handleSubmit = () => {
  if (newItem.value.food_name.trim() && newItem.value.food_type.trim()) {
    emit('item-added', { ...newItem.value });
    newItem.value = { food_name: '', expiration_days: 0, food_type: '' };
    emit('close');
  }
};
</script>

<style scoped>
.form-container {
  background-color: var(--darkerMountainShadow);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--freshVeg);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: var(--glacierWater);
  font-size: large;
}

input, select {
  width: 100%;
  padding: 20px;
  border: 3px solid var(--lighterMountainShadow);
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 16px;
  background-color: var(--cloudyTransparent);
  color: var(--darkerMountainShadow);
}

input:focus, select:focus {
  border-color: var(--freshVeg);
  color: black;
  outline: none;
}

.form-actions {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.btn-primary {
  background-color: #4caf50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-secondary {
  background-color: #f44336;
  color: white;
}

.btn-secondary:hover {
  background-color: #e53935;
}
</style>