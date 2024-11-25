<template>
  <div class="welcome-container">
    <h1 class="app-title">Welcome to Grocery Buddy</h1>
    <h3 class="tagline">Your smart assistant for hassle-free grocery shopping!</h3>
    
    <p class="description">With Grocery Buddy, you can:</p>
    <ul class="feature-list">
      <li>🛒 Add and track all food items purchased</li>
      <li>💀 Get updates on nearly expired food items</li>
      <li>📜 Get recipe ideas for your current food items</li>
      <li>🧮 Get stats on food item usage</li>
    </ul>

    <div class="button-container">
      <button @click="goToGroceryList" class="btn get-started">
        Get Started
      </button>

      <button @click="goToProfile" class="btn get-started">
        Profile Page
      </button>

      <button @click="toggleSignupForm" class="btn get-started">
        {{ showSignupForm ? '' : ' Sign Up' }}
      </button>
    </div>

    <!-- Popup form to sign up -->
    <div v-if="showSignupForm" class="popup-overlay" @click="toggleSignupForm">
      <div class="popup-content" @click.stop>
        <CreateProfile @close="toggleSignupForm" />
      </div>
    </div>  

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CreateProfile from '../components/CreateProfile.vue';

const router = useRouter();
const showSignupForm = ref(false);

const goToGroceryList = () => {
  router.push('/add');
};

const goToProfile = () => {
  router.push({ name: 'profile' });
};

const toggleSignupForm = () => {
  showSignupForm.value = !showSignupForm.value;
};
</script>

<style scoped>
.welcome-container {
  text-align: center;
  padding: 20px;
}

.app-title {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.tagline {
  font-size: 1.5em;
  margin-bottom: 20px;
}

.description {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.feature-list {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

.feature-list li {
  font-size: 1.1em;
  margin-bottom: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 10px; /* Adjust the gap between buttons as needed */
  margin-top: 20px;
}

.btn {
  background-color: #4caf50;
  color: white;
  border: solid 1px var(--glacierWater);    
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1em;
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.btn:hover {
  background-color: #45a049;
}

.get-started {
  margin-top: 20px;
}
</style>
