<template>
    <div class="settings">
      <h2>Settings</h2>
  
      <div class="setting-item">
        <label>Password:</label>
        <input v-model="password" type="password" placeholder="Enter new password" />
        <button @click="updatePassword">Change Password</button>
      </div>
  
      <div class="setting-item">
        <label>Email:</label>
        <input v-model="email" type="email" :placeholder="user.email" />
        <button @click="updateEmail">Change Email</button>
      </div>
  
      <div class="setting-item">
        <label>Phone Number:</label>
        <input v-model="phoneNumber" type="tel" :placeholder="user.phone_number" />
        <button @click="updatePhoneNumber">Change Phone Number</button>
      </div>
  
      <div class="setting-item">
        <label>Notification Settings:</label>
        <select v-model="receiveSMS">
          <option :value="true">Enable SMS Notifications</option>
          <option :value="false">Disable SMS Notifications</option>
        </select>
        <button @click="updateNotificationSettings">Update Notifications</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    props: {
      user: {
        type: Object,
        required: true,
      },
    },
    setup(props) {
      const password = ref('');
      const email = ref(props.user.email);
      const phoneNumber = ref(props.user.phone_number);
      const receiveSMS = ref(props.user.receive_sms_notifications);
  
      const updatePassword = async () => {
        await updateUserSetting({ password: password.value });
      };
  
      const updateEmail = async () => {
        await updateUserSetting({ email: email.value });
      };
  
      const updatePhoneNumber = async () => {
        await updateUserSetting({ phone_number: phoneNumber.value });
      };
  
      const updateNotificationSettings = async () => {
        await updateUserSetting({ receive_sms_notifications: receiveSMS.value });
      };
  
      return {
        password,
        email,
        phoneNumber,
        receiveSMS,
        updatePassword,
        updateEmail,
        updatePhoneNumber,
        updateNotificationSettings,
      };
    },
  };
  </script>
  