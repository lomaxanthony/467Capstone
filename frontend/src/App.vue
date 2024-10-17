<template>
  <div id="app">
    <h1>Grocery Buddy</h1>
    <ul>
      <li v-for="item in groceries" :key="item.id">
        {{ item.name }} - Quantity: {{ item.quantity }}
      </li>
    </ul>
    <input v-model="newItem.name" placeholder="New item name" />
    <input v-model.number="newItem.quantity" type="number" placeholder="Quantity" />
    <button @click="addItem">Add Item</button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const groceries = ref([]);
    const newItem = ref({ name: '', quantity: 1 });

    const fetchGroceries = async () => {
      const response = await fetch('http://127.0.0.1:5000/api/groceries');
      groceries.value = await response.json();
    };

    const addItem = async () => {
      await fetch('http://127.0.0.1:5000/api/groceries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...newItem.value, id: groceries.value.length + 1 }),
      });
      groceries.value.push({ ...newItem.value, id: groceries.value.length + 1 });
      newItem.value = { name: '', quantity: 1 };
    };

    onMounted(fetchGroceries);

    return { groceries, newItem, addItem };
  },
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
