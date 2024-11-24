<template>
  <main>
    <div v-if="!loggedIn">
      <h2>Please log in</h2>
      <form @submit.prevent="login">
        <input v-model="username" type="text" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
    </div>
    <div v-else>
      <Profile :user="user" />
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Profile from '../components/Profile.vue';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

const user = ref(null);
const loggedIn = ref(false);
const username = ref('');
const password = ref('');

const checkLogin = async () => {
  try {
    console.log('Checking login status...');
    const token = localStorage.getItem('access_token');
    console.log('Token:', token);
    if (!token) {
      loggedIn.value = false;
      console.log('No token found, setting loggedIn to false');
      return;
    }
    const response = await fetch(`${API_BASE_URL}/check_login`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      credentials: 'include' // Include cookies in the request
    });
    const data = await response.json();
    console.log('Response data:', data);
    loggedIn.value = data.logged_in;
    if (data.logged_in) {
      user.value = data.user;
      console.log('User data:', user.value);
    } else {
      console.log('User is not logged in');
    }
  } catch (error) {
    console.error('Error checking login status:', error);
  }
};

// Check login status on mount
onMounted(() => {
  console.log('Component mounted, calling checkLogin');
  checkLogin();
});
</script>

<style scoped>

</style>