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
      user: null,
      isLoggedIn: false,
    });

    // provide state object to child components
    provide("state", state)

    const router = useRouter();

    // we want to check first if there is a current session logged in
    const fetchSessionData = async () => {
      try {
        // fetch the session status from the /api/session endpoint
        const sessionResponse = await fetch("http://127.0.0.1:5000/api/session", {
          method: "GET",
          credentials: "include",
        });

        if (sessionResponse.ok) {
          const sessionData = await sessionResponse.json();
          if (sessionData.username) {
            // if the session contains a username, the user is logged in
            state.isLoggedIn = true;
            state.user = { user_name: sessionData.username };
            
            // fetch user data
            await fetchUserData(sessionData.username);
          } else {
            state.isLoggedIn = false;
            state.user = null;
          }
        } else {
          state.isLoggedIn = false;
          state.user = null;
        }
      } catch (error) {
        console.error("Error checking session data:", error);
        state.isLoggedIn = false;
        state.user = null;
      }
    };

    // fetch the user data based on the username
    const fetchUserData = async () => {
      try {
        const userResponse = await fetch("http://127.0.0.1:5000/api/user", {
          method: "GET",
          credentials: "include", 
        });

        if (userResponse.ok) {
          const userData = await userResponse.json();
          state.user = userData;
        } else {
          console.error("Error fetching user data:", await userResponse.text());
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    // handle user log out
    const handleLogout = async () => {
      try {
        const logoutResponse = await fetch("http://127.0.0.1:5000/api/logout", {
          method: "POST", // 
          credentials: "include",
        });

        if (logoutResponse.ok) {
          state.isLoggedIn = false;
          state.user = null;
          router.push("/");
        } else {
          console.error("Error logging out:", await logoutResponse.text());
        }
      } catch (error) {
        console.error("Error logging out:", error);
      }
    };

    // on component mount, check session and fetch user data if logged in
    onMounted(() => {
      fetchSessionData();
    });

    return {
      state,
      router,
      handleLogout
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