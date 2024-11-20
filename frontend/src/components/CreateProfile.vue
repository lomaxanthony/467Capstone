<template>
    <div class="create-profile">
      <h2>Create Profile</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="username">Username</label>
          <input v-model="username" type="text" id="username" required />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input v-model="email" type="email" id="email" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input v-model="password" type="password" id="password" required />
        </div>
        <div class="form-group">
          <label for="first_name">First Name</label>
          <input v-model="first_name" type="text" id="first_name" required />
        </div>
        <div class="form-group">
          <label for="last_name">Last Name</label>
          <input v-model="last_name" type="text" id="last_name" required />
        </div>
        <div class="form-group">
          <label for="profile_pic_url">Profile Picture URL</label>
          <input v-model="profile_pic_url" type="text" id="profile_pic_url" />
        </div>
        <div class="form-group">
          <label for="phone_number">Phone Number</label>
          <input v-model="phone_number" type="text" id="phone_number" required />
        </div>
        <div class="form-group">
          <label for="receive_sms_notifications">Receive SMS Notifications</label>
          <input v-model="receive_sms_notifications" type="checkbox" id="receive_sms_notifications" />
        </div>
        <div class="form-group">
          <label for="receive_email_notifications">Receive Email Notifications</label>
          <input v-model="receive_email_notifications" type="checkbox" id="receive_email_notifications" />
        </div>
        <div class="form-group">
          <label for="preferred_notification_time">Preferred Notification Time</label>
          <input v-model="preferred_notification_time" type="time" id="preferred_notification_time" required />
        </div>
        <button type="submit">Create Profile</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';

  const API_BASE_URL = 'http://127.0.0.1:5000/api';
  
  const username = ref('');
  const email = ref('');
  const password = ref('');
  const first_name = ref('');
  const last_name = ref('');
  const profile_pic_url = ref('');
  const phone_number = ref('');
  const receive_sms_notifications = ref(false);
  const receive_email_notifications = ref(false);
  const preferred_notification_time = ref('');
  
  const submitForm = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_name: username.value,
          email: email.value,
          password: password.value,
          first_name: first_name.value,
          last_name: last_name.value,
          profile_pic_url: profile_pic_url.value,
          phone_number: phone_number.value,
          receive_sms_notifications: receive_sms_notifications.value,
          receive_email_notifications: receive_email_notifications.value,
          preferred_notification_time: preferred_notification_time.value
        })
      });
      if (!response.ok) {
        throw new Error('Failed to create profile');
      }
      const data = await response.json();
      console.log('Profile created:', data);
    } catch (error) {
      console.error('Error creating profile:', error);
    }
  };
  </script>
  
  <style scoped>
  .create-profile {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  button {
    padding: 10px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>