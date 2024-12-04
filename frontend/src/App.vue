<!-- 
 
Added a Bootstrap NavBar that we can change if we want. Just wanted some okay looking formating to use while testing

-->


<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">Grocery Buddy</router-link>

        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav" 
          aria-controls="navbarNav" 
          aria-expanded="false" 
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link" active-class="active">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/add" class="nav-link" active-class="active">My Pantry</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/recipes" class="nav-link" active-class="active">Recipes</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/stats" class="nav-link" active-class="active">Stats</router-link>
            </li>
            <li class="nav-item" v-if="state.isLoggedIn">
              <router-link to="/profile" class="nav-link" active-class="active">User Profile</router-link>
            </li>
            <li class="nav-item" v-if="state.isLoggedIn">
              <a href="#" class="nav-link" @click.prevent="handleLogout">Log Out</a>
            </li>
            <li class="nav-item" v-else>
              <router-link to="/login" class="nav-link" active-class="active">Log In</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <router-view></router-view>
  </div>
</template>


<script>
import { reactive, provide, onMounted } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "App",
  setup() {
    const state = reactive({
      user: {
        username: null, // Initialize as null
      },
      isLoggedIn: false,
    });

    provide("state", state);

    const router = useRouter();

    const fetchSessionData = async () => {
      try {
        const response = await fetch("/api/session", {
          method: "GET",
          credentials: "include",
        });

        if (response.ok) {
          const sessionData = await response.json();
          if (sessionData.username) { // Ensure backend sends 'username'
            state.isLoggedIn = true;
            state.user.username = sessionData.username; // Set username
          } else {
            state.isLoggedIn = false;
            state.user.username = null;
          }
        } else {
          state.isLoggedIn = false;
          state.user.username = null;
        }
      } catch (error) {
        console.error("Error fetching session data:", error);
        state.isLoggedIn = false;
        state.user.username = null;
      }
    };

    const handleLogout = async () => {
      try {
        const logoutResponse = await fetch("/api/logout", {
          method: "POST",
          credentials: "include",
        });

        if (logoutResponse.ok) {
          state.isLoggedIn = false;
          state.user.username = null;
          router.push("/login");
        } else {
          console.error("Error logging out:", await logoutResponse.text());
        }
      } catch (error) {
        console.error("Error logging out:", error);
      }
    };

    onMounted(() => {
      fetchSessionData();
    });

    return {
      state,
      handleLogout,
    };
  },
};
</script>


<style scoped>
@import 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css';


.navbar-brand {
  font-weight: bold;
  font-size: 1.8rem;
  color: var(--freshVeg)
}

.navbar-nav .nav-link {
  font-size: 1.1rem;
  margin-right: 15px;
}

.nav-link.active {
  text-decoration: underline;
}

@media (max-width: 992px) {
  .navbar-nav {
    text-align: center;
  }
}
</style>