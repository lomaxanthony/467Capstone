<template>
  <div class="main">
    <h1 class="app-title">Welcome, {{ user ? user.name : 'User' }}</h1>
    <nav class="nav">
      <button @click="selectedView = 'UserProfile'">Profile</button>
      <button @click="selectedView = 'Settings'">Settings</button>
    </nav>
    <component :is="selectedView" :user="user"></component>
  </div>
</template>

<script>
import { ref } from 'vue';
import Settings from './Settings.vue';
import Profile from './Profile.vue';

export default {
  components: {
    Settings
  },
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  setup() {
    const selectedView = ref('Profile'); // Start with UserProfile by default

    return { selectedView };
  }
};
</script>
