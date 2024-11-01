<template>
    <div class="main">
      <h1 class="app-title">Welcome, User</h1>
      <nav class="nav">
        <button @click="selectedView = 'Profile'">Profile</button>
        <button @click="selectedView = 'Settings'">Settings</button>
      </nav>
      <component :is="selectedView"></component>
    </div>
  </template>

<script>
import { ref } from 'vue';
import Profile from './Profile.vue';
import Settings from './Settings.vue';

export default {
  components: {
    Profile,
    Settings
  },
  setup() {
    const selectedView = ref('Profile'); // Start with Profile by default

    return { selectedView };
  }
};
</script>

  <style>
  @media (min-width: 1024px) {
    .main {
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
  }
  </style>