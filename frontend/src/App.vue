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
              <router-link to="/profile" class="nav-link" active-class="active">User Profile</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <router-view></router-view>
  </div>
</template>


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