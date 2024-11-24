<template>
    <div class="login-container">
      <h1>Log In</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="user_name"
            placeholder="Enter your username"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>
  
        <button type="submit" class="btn">Login</button>
      </form>
  
      <div v-if="message" class="message" :class="{ error: isError }">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';

  const API_BASE_URL = 'http://127.0.0.1:5000/api';
  
  const user_name = ref('');
  const password = ref('');
  const message = ref('');
  const isError = ref(false);
  
  const router = useRouter();
  
  const handleLogin = async () => {
    try {
      // Reset message and error state
      message.value = '';
      isError.value = false;
  
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_name: user_name.value,
          password: password.value,
        }),
        credentials: 'include', // Include cookies in the request
      });
  
      const result = await response.json();
  
      if (response.ok) {
      // Store the access token in localStorage
      localStorage.setItem('access_token', result.access_token);
      console.log('access_token:', result.access_token);
        // Login successful, redirect to pantry page
        router.push('/add');
      } else {
        // Login failed, show error message
        message.value = result.message || 'Login failed';
        isError.value = true;
      }
    } catch (error) {
      console.error('Error during login:', error);
      message.value = 'An error occurred during login';
      isError.value = true;
    }
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 1em;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 1em;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  label {
    display: block;
    margin-bottom: 0.5em;
  }
  
  input {
    width: 100%;
    padding: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .btn {
    display: block;
    width: 100%;
    padding: 0.5em;
    color: #fff;
    background-color: #4caf50;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #218a56;
  }
  
  .message {
    margin-top: 1em;
    padding: 0.5em;
    border-radius: 4px;
    text-align: center;
  }
  
  .message.error {
    background-color: #f8d7da;
    color: #842029;
  }
  
  .message:not(.error) {
    background-color: #d1e7dd;
    color: #0f5132;
  }
  </style>
  