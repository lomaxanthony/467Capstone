<template>
    <div class="login-container">
      <h1>Log In</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="user_name"
            placeholder="Enter your username"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>
  
        <button type="submit" class="btn">Login</button>
      </form>
  
      <div v-if="message" class="message" :class="{ error: isError }">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Login",
    data() {
      return {
        user_name: "",
        password: "",
        message: "",
        isError: false,
      };
    },
    methods: {
      async handleLogin() {
        try {
          this.message = "";
          this.isError = false;
  
          // send request to login route with user + pass
          const response = await fetch("http://127.0.0.1:5000/api/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              user_name: this.user_name,
              password: this.password,
            }),
            credentials: "include",
          });
  
          const result = await response.json();
  
          if (response.ok) {
            this.message = "Login successful!";
            this.isError = false;

            // redirect user back to welcome page on success, update message
            this.$router.push("/");

          } else {
            this.message = result.Message || "An error occurred.";
            this.isError = true;
          }
        } catch (error) {
          this.message = "An error occurred while connecting to the server.";
          this.isError = true;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 1em;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 1em;
  }
  
  .form-group {
    margin-bottom: 1em;
  }
  
  label {
    display: block;
    margin-bottom: 0.5em;
  }
  
  input {
    width: 100%;
    padding: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .btn {
    display: block;
    width: 100%;
    padding: 0.5em;
    color: #fff;
    background-color: #4caf50;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #218a56;
  }
  
  .message {
    margin-top: 1em;
    padding: 0.5em;
    border-radius: 4px;
    text-align: center;
  }
  
  .message.error {
    background-color: #f8d7da;
    color: #842029;
  }
  
  .message:not(.error) {
    background-color: #d1e7dd;
    color: #0f5132;
  }
  </style>
  