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

    <button @click="goToGroceryList" class="btn1 get-started">
      Get Started
    </button>

    <button @click="goToProfile" class="btn2 get-started">
      Profile Page
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

    const goToProfile = () => {
      router.push({ name: 'profile' });
    };

    return {
      goToGroceryList,
      goToProfile
    };
  }
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

.btn1 {
  background-color: #4caf50;
  color: white;
  border: solid 3px --var glacier;    
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1em;
  margin: 20px 0; 
}

.btn2 {
  background-color: #4caf50;
  color: white;
  border: solid 3px --var glacier;    
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1em;
  margin: 20px 0; 
}

.btn:hover {
  background-color: #45a049;
}

.get-started {
  margin-top: 20px;
}
</style>
