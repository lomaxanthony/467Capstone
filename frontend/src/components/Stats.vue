<template>
  <div v-if="state && state.user && state.user.username">
    <h2>Stats</h2>
    
    <div>
      <h3>Top Spoiled Foods</h3>
      <ul>
        <li v-for="item in suggestions.top_spoiled" :key="item.food_id">
          Food: {{ item.food_name }} - Times Spoiled: {{ item.times_spoiled }}
        </li>
      </ul>
    </div>
    
    <div>
      <h3>Top Used Foods</h3>
      <ul>
        <li v-for="item in suggestions.top_used" :key="item.food_id">
          Food: {{ item.food_name }} - Times Used: {{ item.times_used }}
        </li>
      </ul>
    </div>
  </div>
  
  <div v-else>
    <p>Loading user data...</p>
  </div>
</template>

<script>
import { inject, watch, onMounted, reactive } from "vue";

export default {
  name: "Stats",
  setup() {
    const state = inject("state");
    const suggestions = reactive({
      top_spoiled: [],
      top_used: [],
    });

    const fetchSuggestions = async () => {
      try {
        if (!state.user || !state.user.username) {
          console.warn("Username is not available.");
          return;
        }

        console.log("Fetching suggestions for user:", state.user.username);
        const response = await fetch(`/api/suggestions/${state.user.username}`, {
          credentials: 'include'
        });

        if (!response.ok) {
          const error = await response.json();
          console.error("API Error:", error);
          throw new Error(error.Error);
        }

        const data = await response.json();
        console.log("Fetched suggestions:", data);
        suggestions.top_spoiled = data.top_spoiled;
        suggestions.top_used = data.top_used;
      } catch (err) {
        console.error("Error fetching suggestions:", err);
      }
    };

    watch(
      () => state.user.username,
      (newUsername) => {
        if (newUsername) {
          fetchSuggestions();
        }
      },
      { immediate: true }
    );

    onMounted(() => {
      fetchSuggestions();
    });

    return { state, suggestions };
  },
};
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 20px;
}

h3 {
  color: #555;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
}
</style>
