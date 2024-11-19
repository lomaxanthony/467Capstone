<template>
  <main>
    <ItemList :items="groceries" /> 
    
    <div class="button-group">
      <button @click="toggleAddForm" class="action-btn">
        {{ showAddForm ? '➖' : '➕ Add Items' }}
      </button>
      <button @click="toggleDeleteForm" class="action-btn">
        {{ showDeleteForm ? '➖' : '🗑️ Delete Items' }}
      </button>
      <button @click="toggleUploadForm" class="action-btn">
        {{ showUploadForm ? '➖' : '📷 Upload Image' }}
      </button>
    </div>

    <div v-if="showAddForm" class="popup-overlay" @click="toggleAddForm">
      <div class="popup-content" @click.stop>
        <AddItem @item-added="addItemToList" @close="toggleAddForm" />
      </div>
    </div>

    <div v-if="showDeleteForm" class="popup-overlay" @click="toggleDeleteForm">
      <div class="popup-content" @click.stop>
        <DeleteItem :items="groceries" @delete-items="deleteItems" @close="toggleDeleteForm" />
      </div>
    </div>

    <div v-if="showUploadForm" class="popup-overlay" @click="toggleUploadForm">
      <div class="popup-content" @click.stop>
        <UploadImage @close="toggleUploadForm" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import AddItem from '../components/AddItem.vue';
import ItemList from '../components/ItemList.vue';
import DeleteItem from '@/components/DeleteItem.vue';
import UploadImage from '../components/UploadImage.vue';

const groceries = ref([]);
const showAddForm = ref(false);
const showDeleteForm = ref(false);
const showUploadForm = ref(false);


// Fetch groceries from the API
const fetchGroceries = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/groceries');
    const data = await response.json();
    console.log('API Response:', data); 
    groceries.value = Array.isArray(data) ? data : []; 
  } catch (error) {
    console.error('Failed to fetch groceries:', error);
  }
};

// Add new item to list 
const addItemToList = async (newItem) => {
  try {

    const response = await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newItem),
    });
    
    if (!response.ok) {
      throw new Error('Failed to add item to the database');
    }

    // Add to local state after successful response
    groceries.value.push(newItem);
    
    toggleAddForm();
  } catch (error) {
    console.error('Failed to add item:', error);
  }
};

// Delete items from list and persist
const deleteItems = async (selectedItems) => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ item_ids: selectedItems })
    });

    if (!response.ok) {
      throw new Error('Failed to delete items from the database');
    }

    // Remove items from local state after successful response
    groceries.value = groceries.value.filter(item => !selectedItems.includes(item.id));
  } catch (error) {
    console.error('Failed to delete items:', error);
  }
};

// Toggle Add Form
const toggleAddForm = () => {
  showAddForm.value = !showAddForm.value;
};

// Toggle Delete Form
const toggleDeleteForm = () => {
  showDeleteForm.value = !showDeleteForm.value;
};

// Toggle Upload Form
const toggleUploadForm = () => {
  showUploadForm.value = !showUploadForm.value;
};

// Fetch groceries from API to get the latest data
onMounted(async () => {  
  await fetchGroceries();
});
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
}

.action-btn {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

/* Popup overlay for the form */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

/* Popup content styling */
.popup-content {
  background-color: var(--lighterMountainShadow);
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  max-width: 95%;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}
</style>