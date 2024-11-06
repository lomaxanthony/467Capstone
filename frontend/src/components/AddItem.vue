<!--

The AddItem component contains the pop-up form to add groceries (still needs more formating/styling)

-->



<template>
  <div class="item-form">
    // prevent the default form from being submitted
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <input
          v-model="newItem.name"
          placeholder="New item name"
          type="text"
          required
          class="form-input"
        />
        <input
          v-model.number="newItem.quantity"
          type="number"
          min="1"
          placeholder="Quantity"
          required
          class="form-input"
        />
      </div>
      <div class="button-group">
        <button type="submit" class="btn btn-primary">Add Item</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newItem = ref({ name: '', quantity: 1 });

// make sure new item is legit then make it the newItem value
const handleSubmit = () => {
  if (newItem.value.name.trim()) {
    newItem.value = { name: '', quantity: 1 }; 
  }
};

</script>

<style>
#app {
  font-family: Arial, sans-serif;
  margin: 2rem;
}
input {
  margin: 0.5rem;
}
</style>
