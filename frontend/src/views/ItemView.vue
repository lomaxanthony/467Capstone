<template>
  <div>
    <main>

      <!-- Call ItemList Component -->
      <ItemList :items="groceries" />


      <div class="button-group">
        <button @click="toggleAddForm" class="action-btn">
          {{ showAddForm ? '➖' : '➕ Add Item' }}
        </button>
        <button @click="toggleDeleteForm" class="action-btn">
          {{ showDeleteForm ? '➖' : '🗑️ Delete Item' }}
        </button>
        <button @click="toggleUploadForm" class="action-btn">
          {{ showUploadForm ? '➖' : '📷 Upload Image' }}
        </button>
      </div>

      <div v-if="showAddForm" class="popup-overlay" @click="toggleAddForm">
        <div class="popup-content" @click.stop>
          <AddItem @item-added="handleItemAdded" @close="toggleAddForm" />
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
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import AddItem from '../components/AddItem.vue';
import DeleteItem from '../components/DeleteItem.vue';
import UploadImage from '../components/UploadImage.vue';
import ItemList from '@/components/ItemList.vue';

const groceries = ref([]);
const showAddForm = ref(false);
const showDeleteForm = ref(false);
const showUploadForm = ref(false);
// const username = ref('');
const isLoggedIn = ref(false);
const router = useRouter();

// // Watch for changes to the groceries array
// watch(newItem, function(newVal) {
//   console.log('New item:', newVal); // Debugging log
// });


// Handle item-added event to get food ID
async function handleItemAdded(newItem) {
  console.log('Handling item-added event with:', newItem); // Debugging log
  try {
    console.log('Fetching food ID for:', newItem.food_name); // Debugging log
    console.log('newItem.food_name: ', typeof newItem.food_name); // Debugging log
    // Make an API call to get the food ID by name
    const response = await fetch(`http://127.0.0.1:5000/api/${String(newItem.food_name)}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch food ID');
    }
    const data = await response.json();
    const food_id = data[0].food_id;
    const food_exp_days = data[0].expiration_days;

    // Add the food ID to the new item
    console.log('food_id; ', food_id)
    console.log('food_exp_days: ', food_exp_days)
    const itemWithFoodId = { ...newItem, food_id: food_id, expiration_days: food_exp_days };
    addItem(itemWithFoodId);
  } catch (error) {
    console.error('Failed to fetch food ID:', error);
  }
}

// Add the new item object above to the user's grocery SQL table
async function addItem(newItem) {
  try {
    console.log('Sending new item to backend:', newItem); // Debugging log
    console.log('newItem.food_id: ', newItem.food_id); // Debugging log 
    const response = await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },      
      body: JSON.stringify(newItem)
    });

    if (!response.ok) {
      throw new Error('Failed to add item to the database');
    }

    const addedItem = await response.json(); // Ensure the response is parsed as JSON
    console.log('Received response from backend:', addedItem); // Debugging log

    // Add to local state after successful response
    groceries.value.push(addedItem); // Ensure groceries is an array
    
    toggleAddForm();
  } catch (error) {
    console.error('Failed to add item:', error);
  }
}
// // Add item to list (used by AddItem component)
// const addItemToList = (newItem) => {
//   console.log('Adding item to list:', newItem); // Debugging log
//   addItem(newItem);
// };

// Delete items from list and persist
async function deleteItems(selectedItems) {
  try {
    console.log('Deleting items:', selectedItems); // Debugging log
    for (const itemId of selectedItems) {
      const response = await fetch(`http://127.0.0.1:5000/api/groceries/${itemId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to delete item with ID ${itemId}`);
      }

      console.log(`Item with ID ${itemId} deleted successfully`); // Debugging log
    }

    // Remove items from local state after successful response
    groceries.value = groceries.value.filter(item => !selectedItems.includes(item.id));
  } catch (error) {
    console.error('Failed to delete items:', error);
  }
}

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
const fetchGroceries = async () => {
  try {
    console.log('Fetching groceries from backend'); // Debugging log
    const response = await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    
    // Explicitly set as an array because List component expects an array
    groceries.value = Array.isArray(data) ? data : [];
    
    console.log('Fetched groceries:', groceries.value); // Debugging log
  } catch (error) {
    console.error('Failed to fetch groceries:', error);
  }
};

// Check if user is logged in
async function checkLogin() {
  try {
    console.log('Checking login status'); // Debugging log
    const response = await fetch('http://127.0.0.1:5000/api/session', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    isLoggedIn.value = data.logged_in;
    if (!isLoggedIn.value) {
      router.push('/login'); // Redirect to login page if not logged in
    }
  } catch (error) {
    console.error('Failed to check login status:', error);
  }
}

onMounted(async () => { 
  await checkLogin(); 
  if (isLoggedIn.value) {
    await fetchGroceries();
  }
});
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background-color: var(--MountainShadow);
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
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: rgb(56, 59, 59);
  padding: 40px;
  border-radius: 8px;
}
</style> 
