<template>
    <div>
      <form @submit.prevent="handleSubmit">
      <input v-model="newItem.name" placeholder="New item name" />
      <input v-model.number="newItem.quantity" type="number" placeholder="Quantity" />
      <button @click="addItem">Add Item</button>
      <button type="button" @click="$emit('close')">Cancel</button>
    </form>
    </div>
  </template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['item-added', 'close']);
const newItem = ref({ name: '', quantity: 1 });

const handleSubmit = () => {
  if (newItem.value.name.trim()) {
    emit('item-added', { ...newItem.value }); 
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
