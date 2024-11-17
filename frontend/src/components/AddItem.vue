<!--

The AddItem component contains the pop-up form to add groceries (still needs more formating/styling)

-->



<template>
  <div>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="food_name">Food Name</label>
        <input id="food_name" v-model="newItem.food_name" placeholder="eg: tomatoes" required />
      </div>
      <div>
        <label for="expiration_days">Expiration Days</label>
        <input id="expiration_days" v-model.number="newItem.expiration_days" type="number" placeholder="Expiration Days" required />
      </div>
      <div>
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
      <button type="submit">Add Item</button>
      <button type="button" @click="$emit('close')">Cancel</button>
    </form>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['item-added', 'close']);
const newItem = ref({ food_name: '', expiration_days: 0, food_type: ''});

const handleSubmit = () => {
  if (newItem.value.food_name.trim() && newItem.value.food_type.trim()) {
    emit('item-added', { ...newItem.value });
    newItem.value = { food_name: '', expiration_days: 0, food_type: ''};
    emit('close');
  }
};
</script>

<style scoped>

form div {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: black;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
</style>
