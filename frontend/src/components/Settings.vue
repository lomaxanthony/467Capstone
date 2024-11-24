<template>
  <div class="settings-container" v-if="state.user">
    <h2>Settings</h2>

    <form @submit.prevent>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          v-model="password"
          id="password"
          type="password"
          placeholder="Enter new password"
        />
        <button @click="updatePassword" type="button" class="btn">Change Password</button>
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input
          v-model="email"
          id="email"
          type="email"
          :placeholder="state.user.email"
        />
        <button @click="updateEmail" type="button" class="btn">Change Email</button>
      </div>

      <div class="form-group">
        <label for="phoneNumber">Phone Number:</label>
        <input
          v-model="phoneNumber"
          id="phoneNumber"
          type="tel"
          :placeholder="state.user.phone_number"
        />
        <button @click="updatePhoneNumber" type="button" class="btn">Change Phone Number</button>
      </div>

      <div class="form-group">
        <label for="notification">Notification Settings:</label>
        <select v-model="receiveSMS" id="notification">
          <option :value="true">Enable SMS Notifications</option>
          <option :value="false">Disable SMS Notifications</option>
        </select>
        <button @click="updateNotificationSettings" type="button" class="btn">
          Update Notifications
        </button>
      </div>
    </form>
  </div>
  <div v-else>
    Loading user data...
  </div>
</template>


<script>
import { ref, inject } from "vue";

export default {
  setup() {
    // inject state from app.vue
    const state = inject("state");

    const password = ref("");
    const email = ref(state.user?.email || ""); 
    const phoneNumber = ref(state.user?.phone_number || "");
    const receiveSMS = ref(state.user?.receive_sms_notifications || false);

    const updatePassword = async () => {
      await updateUserSetting({ password: password.value });
    };

    const updateEmail = async () => {
      await updateUserSetting({ email: email.value });
      state.user.email = email.value
    };

    const updatePhoneNumber = async () => {
      await updateUserSetting({ phone_number: phoneNumber.value });
      state.user.phone_number = phoneNumber.value
    };

    const updateNotificationSettings = async () => {
      await updateUserSetting({ receive_sms_notifications: receiveSMS.value });
      state.user.receive_sms_notifications = receiveSMS.value
    };

    const updateUserSetting = async (updateData) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/user`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updateData),
          credentials: 'include',
        });

        if (!response.ok) {
          console.error("Failed to update setting");
        }
      } catch (error) {
        console.error("Error updating setting:", error);
      }
    };

    return {
      state,
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


<style scoped>

.settings-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1em;
  color: white
}

h2 {
  text-align: center;
  margin-bottom: 1em;
}

.form-group {
  margin-bottom: 1.5em;
}

label {
  display: block;
  margin-bottom: 0.5em;
}

input,
select {
  width: 100%;
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Buttons */
.btn {
  display: block;
  width: 100%;
  padding: 0.5em;
  margin-top: 0.5em;
  color: #fff;
  background-color: #4caf50;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
}

.btn:hover {
  background-color: #218a56;
}
</style>