<template>
    <div>
      <h2>Delete Items</h2>
      <div class="grid">
        <div v-for="item in items" :key="item.id" class="grid-item">
          <input type="checkbox" :value="item.id" v-model="selectedItems" />
          <span>{{ item.name }}</span>
        </div>
      </div>
      <button @click="handleDelete">Delete Selected Items</button>
      <button type="button" @click="$emit('close')">Cancel</button>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    items: {
      type: Array,
      required: true
    }
  });
  
  const emit = defineEmits(['delete-items', 'close']);
  const selectedItems = ref([]);
  
  const handleDelete = () => {
    emit('delete-items', selectedItems.value);
    selectedItems.value = [];
    emit('close');
  };
  </script>
  
  <style scoped>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }
  .grid-item {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
  }
  </style>