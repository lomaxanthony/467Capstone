<template>
  <div class="welcome-container">
    <h1 class="app-title">Welcome to Grocery Buddy</h1>
    <h3 class="tagline">Your smart assistant for hassle-free grocery shopping!</h3>
    
    <!-- <img 
      src="@/assets/grocery-buddy-logo.png" 
      alt="Grocery Buddy Logo" 
      class="logo"
    /> -->

    <p class="description">With Grocery Buddy, you can:</p>
    <ul class="feature-list">
      <li>🛒 Add and track all food items purchased</li>
      <li>💀 Get updates on nearly expired food items</li>
      <li>📜 Get recipe ideas for your current food items</li>
      <li>🧮 Get stats on food item usage</li>
    </ul>

    <button @click="goToGroceryList" class="btn get-started">
      Get Started
    </button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const goToGroceryList = () => {
      router.push('/add'); 
    };

    return { goToGroceryList };
  },
};
</script>

<style scoped>
.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--darkerMountainShadow);
  color: #ffffff;
  text-align: center;
  padding: 5%;
  margin-top: 8%;
}

.app-title {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: bold;
}

.description {
  font-size: 1rem;
  margin-bottom: 30px;
  flex-direction: row;
}

.get-started {
  background-color: var(--freshVeg);
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.get-started:hover {
  background-color: #45a047;
}
</style>
