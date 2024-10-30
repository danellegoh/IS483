<template>
    <!-- edit goal popup -->
    <div v-if="visible" class="popupOverlay">
        <div class="card">
            <div class="close-button-container">
                <div class="close-button" @click="closePopup">
                    <i class="uil uil-times"></i>
                </div>
            </div>

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
                v-model:value="localGoalValue"
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
export default {
    props: {
        visible: {
            type: Boolean,
            default: false
        },
        caseType: {
            type: Number,
            default: 0
        },
        goalValue: {
            type: Number,
            default: 150
        }
    },
    data() {
        // const goalValue = ref(150);
        // const caseType = ref(3);
        console.log("visible prop", this.visible);
        console.log("case type received", this.caseType);
        return {
            // goalValue,
            // caseType
            localGoalValue: this.goalValue
        };
    },

    methods: {
        closePopup() {
            this.$emit('close');
        },
        confirmGoal() {
            this.$emit('confirm', this.localGoalValue);
            console.log(`Confirmed new goal: ${this.localGoalValue}`);
        }
    }
};

</script>

<style scoped>
.popupOverlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 20000;
    display: flex;
    justify-content: center;
    align-items: center;
}

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
  position: relative;
}

.close-button-container {
    position: absolute; 
    top: 10px; 
    right: 15px; 
    cursor: pointer; 
}
</style>