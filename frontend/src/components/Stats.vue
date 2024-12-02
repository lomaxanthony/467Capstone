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
            Food ID: {{ item.food_name }} - Times Used: {{ item.times_spoiled }}
            </li>
        </ul>
        </div>
    </div>
    <div v-else>
        <p>Loading user data...</p>
    </div>
</template>

<script>
    import { inject, watch } from "vue";

    export default {
        name: "Stats",
        setup() {
            const state = inject("state");
            return { state }
        },
        data() {
            return {
                suggestions: {
                    top_spoiled: [],
                    top_used: [],
                },
            };
        },
        methods: {
            async fetchSuggestions() {
                try {
                    const response = await fetch(`http://127.0.0.1:5000/api/suggestions/${this.state.user.username}`);
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.Error);
                    }
                    const data = await response.json();
                    this.suggestions = data;
                } catch (err) {
                    console.error(err);
                }
            }
        },
        mounted() {
            watch(
                () => this.state?.user?.username,
                (newUsername) => {
                    if (newUsername) {
                        this.fetchSuggestions();
                    }
                },
                { immediate: true }
            );
        },
    };
</script>