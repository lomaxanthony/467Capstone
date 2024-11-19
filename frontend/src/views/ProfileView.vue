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

const user = ref(null);
const loggedIn = ref(false);
const username = ref('');
const password = ref('');

const checkLogin = async () => {
  try {
    const response = await fetch('/api/check_login', {
      method: 'GET',
      credentials: 'include' // Include cookies in the request
    });
    const data = await response.json();
    loggedIn.value = data.logged_in;
    if (data.logged_in) {
      user.value = data.user;
    }
  } catch (error) {
    console.error('Error checking login status:', error);
  }
};

const login = async () => {
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: username.value, password: password.value }),
      credentials: 'include' // Include cookies in the request
    });
    if (!response.ok) {
      throw new Error('Login failed');
    }
    const data = await response.json();
    user.value = data.user;
    loggedIn.value = true;
  } catch (error) {
    console.error('Error logging in:', error);
  }
};

// Check login status on mount
onMounted(checkLogin);
</script>

<style scoped>

</style>