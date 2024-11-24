<template>
  <div class="main-container">
    <h1 class="app-title">
      Welcome, {{ state?.user ? `${state.user.first_name || ''} ${state.user.last_name || ''}`.trim() || 'User' : 'User' }}
    </h1>
    <nav class="nav">
      <button class="nav-button" @click="selectedView = 'Profile'">Profile</button>
      <button class="nav-button" @click="selectedView = 'Settings'">Settings</button>
    </nav>
    <div class="view-container">
      <component :is="selectedView"></component>
    </div>
  </div>
</template>

<script>
import { ref, inject } from 'vue';
import Profile from './Profile.vue';
import Settings from './Settings.vue';

export default {
  components: {
    Profile,
    Settings
  },
  setup() {
    const selectedView = ref('Profile'); // start with profile by default
    const state = inject("state"); // inject state from app.vue
    return { selectedView, state };
  }
};
</script>

<style scoped>
.main-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1em;
  border-radius: 8px;
  text-align: center;
}

.app-title {
  font-size: 1.8rem;
  margin-bottom: 1em;
  font-weight: bold;
}

.nav {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1.5em;
}

.nav-button {
  padding: 0.5em 1em;
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.nav-button:hover {
  background-color: #218a56;
}

.view-container {
  margin-top: 1em;
  border-radius: 8px;
  padding: 1em;
}
</style>