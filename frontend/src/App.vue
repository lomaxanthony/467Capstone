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
              <router-link to="/profile" class="nav-link" active-class="active">User Profile</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style scoped>
@import 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css';

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%; 
  padding: 20px;
  background-color: var(--mountainShadow);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.8rem;
  color: var(--freshVeg);
}

.navbar-nav .nav-link {
  color: var(--glacierWater);
}

.navbar-nav .nav-link.active {
  font-weight: bold;
  color: var(--freshVeg);
}
</style>