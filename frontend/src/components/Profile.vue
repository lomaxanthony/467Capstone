<template>
    <div class="profile-container" v-if="state.user">
      <h2>Profile</h2>
      <div class="profile-picture">
        <img :src="state.user.profile_pic_url" alt="Profile Picture" />
      </div>
      <div class="profile-info">
        <div class="info-item">
          <strong>Username:</strong> {{ state.user.username }}
        </div>
        <div class="info-item">
          <strong>Email:</strong> {{ state.user.email }}
        </div>
        <div class="info-item">
          <strong>Phone Number:</strong> {{ state.user.phone_number }}
        </div>
      </div>
    </div>
    <div v-else>
      Loading user data...
    </div>
  </template>

<script>
    import { inject } from "vue";

    export default {
        name: "Profile",
        setup() {
            const state = inject("state");
            return { state }
        },

    }
</script>

<style scoped>

.profile-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1em;
  color: #ffffff;
  border-radius: 8px;
  text-align: center;
}

h2 {
  margin-bottom: 1em;
}

.profile-picture img {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 1em;
  border: 2px solid #ccc;
}

.profile-info {
  margin-top: 1em;
}

.info-item {
  margin-bottom: 0.5em;
  font-size: 1rem;
  color: #ffffff;
}

.info-item strong {
  color: #4caf50;
}
</style>
