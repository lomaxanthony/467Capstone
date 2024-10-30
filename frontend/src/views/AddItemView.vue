<template>
  <main>

    <ItemList :items="groceries" /> 
    
    <button @click="toggleForm" class="toggle-btn">
      {{ showForm ? '➕' : '➕' }}
    </button>

    <div v-if="showForm" class="popup-overlay" @click="toggleForm">
      <div class="popup-content" @click.stop>
        <AddItem @item-added="addItemToList" @close="toggleForm" />
      </div>
    </div>
  
  </main>
</template>

<!-- <script setup>
import { ref, onMounted } from 'vue';
import AddItem from '../components/AddItem.vue'
import ItemList from '../components/ItemList.vue';

const groceries = ref([]);
const showForm = ref(false);

// Fetch existing groceries from the API
// will need to change when DB is working
const fetchGroceries = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/groceries');
    groceries.value = await response.json();
  } catch (error) {
    console.error('Failed to fetch groceries:', error);
  }
};

// add new item to list
const addItemToList = (newItem) => {
  groceries.value.push(newItem);
  toggleForm();
};

// show form on click
const toggleForm = () => {
  showForm.value = !showForm.value;
};

// Fetch groceries on component mount
onMounted(fetchGroceries);
</script> -->

<script setup>
import { ref, onMounted, watch } from 'vue';
import AddItem from '../components/AddItem.vue';
import ItemList from '../components/ItemList.vue';

const groceries = ref([]);
const showForm = ref(false);

// Load groceries from localStorage
const loadGroceries = () => {
  const savedGroceries = localStorage.getItem('groceries');
  if (savedGroceries) {
    groceries.value = JSON.parse(savedGroceries);
  }
};

// Save groceries to localStorage
const saveGroceries = () => {
  localStorage.setItem('groceries', JSON.stringify(groceries.value));
};

// Fetch groceries from the API
const fetchGroceries = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/groceries');
    const data = await response.json();
    groceries.value = data;
    saveGroceries(); // Save to localStorage after fetching
  } catch (error) {
    console.error('Failed to fetch groceries:', error);
    // If API fails, load from localStorage as fallback
    loadGroceries();
  }
};

// Add new item to list and persist
const addItemToList = async (newItem) => {
  try {
    // Add to local state
    groceries.value.push(newItem);
    
    // Save to localStorage
    saveGroceries();
    
    // Optional: Sync with backend
    await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newItem),
    });
    
    toggleForm();
  } catch (error) {
    console.error('Failed to add item:', error);
    // Keep the item in local state even if API fails
  }
};

// Show form on click
const toggleForm = () => {
  showForm.value = !showForm.value;
};

// Watch for changes in groceries and save to localStorage
watch(groceries, () => {
  saveGroceries();
}, { deep: true });

// On component mount
onMounted(async () => {
  // First try to load from localStorage for immediate display
  loadGroceries();
  // Then fetch from API to get the latest data
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

.toggle-btn {
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
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  width: 300px;
  max-width: 90%;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}
</style>

