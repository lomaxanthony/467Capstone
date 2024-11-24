// Use this router file to add new page views with a corresponding
// **View.vue file. The View.vue files will call the .vue components from there. 

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserProfileView from '../views/UserProfileView.vue'
import AddItemView from '../views/ItemView.vue'
import LoginView from '@/views/LoginView.vue'
import ProfileView from '../views/ProfileView.vue'
import ItemView from '../views/ItemView.vue'
import RecipeView from '@/views/RecipeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/add',
      name: 'addItems',
      component: ItemView
    },
    {
      path: '/recipes',
      name: 'recipes',
      component: RecipeView
    },
    {
      path: '/profile',
      name: 'profile',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: UserProfileView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      component: ProfileView
    }
  ]
})

export default router
