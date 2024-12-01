<template>
  <div class="form-container">
    <h2>Delete Items</h2>
    <div class="grid">
      <div v-for="item in items" :key="item.id" class="grid-item">
        <input type="checkbox" :value="item.id" v-model="selectedItems" />
        <span>{{ item.name }}</span>
      </div>
    </div>
    <div class="form-actions">
      <button @click="handleDelete" class="btn btn-primary">Delete Selected Items</button>
      <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
    </div>
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

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

.grid-item {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center;
  border-radius: 5px;
  background-color: var(--glacierWater);
}

input[type="checkbox"] {
  margin-right: 10px;
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
