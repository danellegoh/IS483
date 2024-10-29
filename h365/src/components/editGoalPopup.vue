<template>
    <!-- edit goal popup -->
    <div>
        <div class="card">

            <!-- consistently hitting goal -->
            <div class="content" v-if="caseType == 1">
                <i class="uil uil-trophy"></i>
                <p class="head"> You’re Crushing It! </p>
                <p class="body"> You’ve been consistently hitting your goals! 
                    Consider adjusting your target 
                    <span style="font-family: text-bold"> upwards </span> 
                    to keep the momentum going and unlock new heights of success. 
                </p>
            </div>

            <!-- consistently not hitting goal and goal > 150 -->
            <div class="content" v-if="caseType == 2">
                <i class="uil uil-fire"></i>
                <p class="head"> Let’s Refocus. </p>
                <p class="body">
                    Small, achievable steps will help you build momentum towards long-term success. 
                    Considering scaling your targets 
                    <span style="font-family: text-bold"> downwards </span>
                    for a more manageable pace.
                </p>
            </div>

            <!-- consistently not hitting goal and goal == 150 -->
            <div class="content" v-if="caseType == 3">
                <i class="uil uil-mountains-sun"></i>
                <p class="head"> You can do it! </p>
                <p class="body"> Let’s start small and focus on steady progress. 
                    Every small step counts towards building sustainable success! </p>
            </div>

            <div class="container" v-if="caseType == 1 || caseType == 2">
                <n-input-number
                v-model:value="goalValue"
                :min="150" 
                :step="5" 
                show-button
                style="width: 200px"
                />
            </div>

            <div class="coolButton" v-if="caseType == 1 || caseType == 2">
                <button style="background-color: var(--blue);" @click="confirmGoal"> Confirm </button>
            </div>

            <div class="coolButton" v-if="caseType == 3">
                <button style="background-color: var(--blue);" @click="closePopup"> Close </button>
            </div>

        </div>
    </div>

</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const goalValue = ref(150);
        const caseType = ref(3);

        function confirmGoal() {
            console.log(`Confirmed new goal: ${goalValue.value}`);
        }

        return {
            goalValue,
            caseType,
            confirmGoal,
        };
    },

    methods: {
        closePopup() {
            this.$emit('close');
        },
    }
};

</script>

<style scoped>

i {
    font-size: 25px;
}

.coolButton {
    display: flex;
    justify-content: center;
}

button {
    font-family: text-medium;
    color: var(--grey);
    font-size: 10px;
    background-color: var(--blue);
    border-radius: 5px;
    border: none;
    padding: 5px 10px;
    width: 60px;
}

.card {
    width: 90%;
    display: flex;
    margin: auto;
    padding: 20px;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.head {
    font-family: text-bold;
    font-size: 16px;
    color: var(--orange);
    margin-bottom: 10px;
    display: flex;
}

.body {
    font-family: text-regular;
    font-size: 13px;
    text-align: justify;
    margin-bottom: 15px;
    width: 90%;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 16px;
}

</style>