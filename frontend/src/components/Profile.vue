<template>
    <div class="main">
        <img 
            src="https://media.istockphoto.com/id/1495088043/vector/user-profile-icon-avatar-or-person-icon-profile-picture-portrait-symbol-default-portrait.jpg?s=170667a&w=0&k=20&c=LPUo_WZjbXXNnF6ok4uQr8I_Zj6WUVnH_FpREg21qaY="
            width="200"
        >
        <div>Username: {{ user.user_name }}</div>
        <div>Email: {{ user.email }}</div>
        <div>Phone Number: {{ user.phone_number }}</div>
    </div>
  </template>

<script>
    import { reactive } from 'vue'

    export default {
        setup() {
            // using dummy data to test out app

            const user = reactive({
                user_name: 'user123',
                email: 'user@gmail.com',
                phone_number: '123456789',
                receive_sms_notifications: true
            });

            return { user };
        }
    }
</script>

<style>
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
</style>
