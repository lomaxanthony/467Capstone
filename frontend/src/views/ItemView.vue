<template>
  <div>
    <main>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AddItem from '../components/AddItem.vue';
import DeleteItem from '../components/DeleteItem.vue';
import UploadImage from '../components/UploadImage.vue';

const groceries = ref([]);
const showAddForm = ref(false);
const showDeleteForm = ref(false);
const showUploadForm = ref(false);
// const username = ref('');
const isLoggedIn = ref(false);
const router = useRouter();

// Add items to list and persist
const addItem = async (newItem) => {
  try {
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

    // Add to local state after successful response
    groceries.value.push(newItem);
    
    toggleAddForm();
  } catch (error) {
    console.error('Failed to add item:', error);
  }
};

// Add item to list (used by AddItem component)
const addItemToList = (newItem) => {
  console.log('Adding item to list:', newItem); // Debugging log
  addItem(newItem);
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
const fetchGroceries = async () => {
  try {
    console.log('Fetching groceries from backend'); // Debugging log
    const response = await fetch('http://127.0.0.1:5000/api/groceries', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    
    // Explicitly set as an array
    groceries.value = Array.isArray(data) ? data : [];
    
    console.log('Fetched groceries:', groceries.value); // Debugging log
  } catch (error) {
    console.error('Failed to fetch groceries:', error);
  }
};

// Check if user is logged in
const checkLogin = async () => {
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
};

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
