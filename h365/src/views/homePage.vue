<template>
    <div class="stickyHeader">
        <div class="pageHeader">
            <p> Welcome back, 
                <span> {{ userName }} </span> 
            </p>
        </div>

        <div class="displayBlock">
            <div class="blockLeft">
                <div class="blockText">
                    <p style="margin-right: 5px"> {{ numHealthCoins }} </p>
                    <span> <img src="../assets/icons/homepage/coin.png"> </span>
                </div>
                <p> My Healthcoins </p>
            </div>

            <div class="blockRight">
                <div class="blockText">
                    <p> {{ streakCount }} </p>
                    <img src="../assets/icons/homepage/streak.png" style="width: 25px; height: auto; margin-right: 3px;">
                </div>

                <div style="display: flex; align-items: center;">
                    <p style="margin-right: 3px"> Activity Streak </p>
                    <i class="uil uil-info-circle" style="display: flex; align-items: center;"></i>
                </div>
            </div>
        </div>
    </div>

    <div class="pagePad">
        <div class="pageHeading">
            <img src="../assets/icons/homepage/goal.png">
            <div class="headerText">
                <p class="head"> My Weekly Progress </p>
                <p class="body"> Keep pushing towards your goals! </p>
            </div>
        </div>

        <div class="container">
            <div class="basicCard">
                <div class="barLabel">
                    <span class="updatedVar"> {{ currentWeekly }} / {{ goalWeekly }} </span>
                    <span class="updatedText"> minutes of MVPA </span>
                </div>

                <div class="bar">
                    <n-space vertical>
                        <n-progress
                            type="line"
                            :percentage="progressPercentage"
                            :height="20"
                            :border-radius="6"
                            :fill-border-radius="0"
                            :show-indicator="false"
                            color="#FFCE49"
                        />
                    </n-space>
                </div>

                <div class="updateDetails">
                    <button class="syncButton" @click="stravaLogin"> Sync now </button>
                </div>
            </div>

        </div>


        <div class="pageHeading">
            <img src="../assets/icons/homepage/progress.png">
            <div class="headerText">
                <p class="head"> My Daily Progress </p>
                <p class="body"> Stay focused and keep moving forward! </p>
            </div>
        </div>

        <div class="container">
            <div class="basicCard">
                <div class="barLabel" style="padding-bottom: 16px;">
                    <span class="updatedText"> You have worked out for </span>
                    <span class="updatedVar" style="color: var(--purple)"> {{ minutesToday }} </span>
                    <span class="updatedText"> minutes today! </span>
                </div>
            </div>
        </div>


        <div class="pageHeading">
            <img src="../assets/icons/homepage/glass.png">
            <div class="headerText">
                <p class="head"> My H365 Unwrapped </p>
                <p class="body"> Take a look at your progress </p>
            </div>
        </div>

        <div class="container">
            <div class="basicCard">

                <div class="pageHeading">
                    <span style="font-family: text-medium; color: var(--text-highlight); 
                    font-size: 13px; text-align: justify;"> 
                        You moved for a total of 
                        <span style="font-family: text-bold; color: var(--green)"> {{ mr_movingMinutes }} </span>
                        minutes in 
                        <span style="color: var(--orange)"> {{ lastMonth }} </span>
                    </span>
                </div>

                <router-link :to="{ name: 'monthlyReport'}">
                    <button class="syncButton" style="width: 90%;" @click="goToMonthlyReport"> View your {{ lastMonth }} report </button>
                </router-link>

            </div>
        </div>


        <div class="pageHeading">
            <img src="../assets/icons/homepage/bulb.png">
            <div class="headerText">
                <p class="head"> My next steps </p>
                <p class="body"> Personalised tips to reach your health goals </p>
            </div>
        </div>

        <div class="container" v-if="recommendedEvents.length > 0">
            <div class="carousel">
                
                <div v-for="event in recommendedEvents" :key="event.event_id">
                    <router-link :to="{ name: 'viewEventPage', params: { eventId: event.event_id } }">
                        <div class="card drop-shadow">
                            <div class="cardImage">
                                <img src="../assets/icons/homepage/nextSteps.png">
                            </div>
                            <div class="cardText">

                                <!-- v-if few slots left -->
                                <div v-if="event.is_near" class="lowSlotAlert">
                                    Event near you
                                </div>

                                <!-- activity name -->
                                <p class="eventName"> {{ event.title }} </p>

                                <!-- date, day, and time  -->
                                <div class="eventInfo">
                                    <div class=eventDetails>
                                        <p> {{ formattedDate(event.start_date) }} </p>
                                        <p> {{ formattedTime(event.start_date, event.end_date) }} </p>
                                    </div>
                                </div>

                                <!-- location -->
                                <div class="eventInfo">
                                    <div class=eventDetails>
                                        <p> {{ event.location }} </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </router-link>
                </div>

            </div>
        </div>

        <div class="container" v-else>
            <div class="basicCard">

                <div class="pageHeading">
                    <span style="font-family: text-medium; color: var(--text-highlight); 
                    font-size: 13px; text-align: justify;"> 
                        Looks like we don’t have any personalized events for you right 
                        now, but check out the others – you might find something for you! ✨
                    </span>
                </div>

                <router-link :to="{ name: 'eventsPage'}">
                    <button class="syncButton" style="width: 90%"> View All Events </button>
                </router-link>

                </div>
        </div> 

        <PopupGoal
            v-if="showPopup"
            :visible="showPopup"
            :caseType="caseType"
            :goalValue="goalWeekly"
            @close="showPopup = false"
            @confirm="handleGoalChange"
        />
        
    </div>



</template>

<script>
import { useStore } from 'vuex';
import { computed } from 'vue';
import axios from 'axios';
import PopupGoal from '@/components/editGoalPopup.vue';

export default {
    components: {
        PopupGoal
    },
    setup() {
        const store = useStore();
        const userId = computed(() => store.state.userId);
        const userEmail = computed(() => store.state.userEmail);
        
        return {
            userId,
            userEmail
        };
    },
    data() {
        return {
            streakCount: 0,
            weekStarted: 0,
            weekCurrent: 0,
            goalId: 0,

            goalMet: false,
            toPrompt: false,
            showPopup: false,
            caseType: 1,
            localGoalValue: 0,

            currentWeekly: 0,
            goalWeekly: 0,
            minutesToday: 0,
            mr_movingMinutes: 0,
            mr_topActivity: "",
            mr_totalDistance: 0,
            mr_allActivitites: {},
            lastMonth: "",
            numHealthCoins: 0,
            userName: "",
            recommendedEvents: []
        };
    },
    computed: {
        progressPercentage() {
            return this.goalWeekly > 0 ? (this.currentWeekly / this.goalWeekly) * 100 : 0;
        }
    },
    methods: {
        async fetchUserData() {
            try {
                const userResponse = await axios.get(`http://127.0.0.1:5001/user/${this.userEmail}`);
                const userData = userResponse.data.data;
                this.numHealthCoins = userData.total_point;
                this.userName = userData.name;
            } catch (error) {
                console.error("Error fetching user data:", error);
            }
        },
        async fetchRecommendedEvents() {
            if (!this.userId) {
                console.error("User ID is not available");
                return;
            }
            try {
                const response = await axios.get(`http://localhost:5042/user/${this.userId}/eligible-events`);
                if (response.data.code === 200) {
                    const eventIds = response.data.data;
                    const eventDetailsPromises = eventIds.map(id => 
                        axios.get(`http://localhost:5002/event/${id}`)
                    );
                    const eventDetailsResponses = await Promise.all(eventDetailsPromises);

                    // Get current date and time, and calculate "tomorrow"
                    const currentDate = new Date();
                    const tomorrowDate = new Date();
                    tomorrowDate.setDate(currentDate.getDate() + 1);
                    tomorrowDate.setHours(23, 59, 59, 999); // End of tomorrow

                    // Filter events to only include those happening later today or tomorrow
                    this.recommendedEvents = eventDetailsResponses
                        .map(res => res.data.data)
                        .filter(event => {
                            const eventDate = new Date(event.start_date);
                            return eventDate >= currentDate && eventDate <= tomorrowDate;
                        });
                } else {
                    console.error("Failed to fetch eligible events:", response.data.error);
                }
            } catch (error) {
                console.error("Error fetching recommended events:", error);
            }
        },
        formattedDate(dateStr) {
            const date = new Date(dateStr);
            const day = date.getDate();
            const month = new Intl.DateTimeFormat('en-US', { month: 'long' }).format(date);
            const year = date.getFullYear();
            const weekday = new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(date);
            return `${day} ${month} ${year}, ${weekday}`;
        },
        formattedTime(startDateStr, endDateStr) {
            const startDate = new Date(startDateStr);
            const endDate = new Date(endDateStr);
            const formatTime = date => new Intl.DateTimeFormat('en-US', {
                hour: 'numeric',
                minute: 'numeric',
                hour12: true
            }).format(date);
            return `${formatTime(startDate)} - ${formatTime(endDate)}`;
        },
        async stravaLogin() {
            window.location.href = "http://localhost:5020/connect";
            await this.syncNow();
        },
        async syncNow() {
            try {
                const goalResponse = await axios.get(`http://127.0.0.1:5011/goals/${this.userId}`);
                const goalData = goalResponse.data;
                // console.log(goalData)
                const goal_id = goalData[0].goal_id;
                this.goalId = goal_id;

                const streakResponse = await this.$http.get("http://127.0.0.1:5010/streaks/" + goal_id)
                const streakData = streakResponse.data;
                // console.log(streakData)
                const streak_id = streakData["data"][0].streak_id;

                const payload = {
                    goal_id: goal_id,
                    user_id: this.userId,
                    streak_id: streak_id,
                };
                const response = await axios.post('http://localhost:5030/update_streak', payload, {
                    headers: { 'Content-Type': 'application/json' }
                });
                console.log(response.data.data);
                this.streakCount = response.data.data.streak_count;
                this.weekStarted = response.data.data.week_started;
                this.weekCurrent = response.data.data.week_current;
                this.goalMet = response.data.data.goal_met;
                this.toPrompt = response.data.data.to_prompt;

                this.currentWeekly = response.data.data.weekly_time_lapse;
                this.goalWeekly = goalData[0].target;
                this.minutesToday = response.data.data.daily_time_lapse;
                this.mr_movingMinutes = response.data.data.monthly_time_lapse;
                this.mr_topActivity = response.data.data.monthly_top_activity;
                this.mr_totalDistance = response.data.data.monthly_distance;
                this.mr_allActivitites = response.data.data.activities_in_month;
            } catch (error) {
                console.error('Sync failed:', error);
            }
        },
        goToMonthlyReport() {
            this.$router.push({
                name: 'monthlyReport',
                params: {
                    streakCount: this.streakCount,
                    mr_movingMinutes: this.mr_movingMinutes,
                    mr_topActivity: this.mr_topActivity,
                    mr_totalDistance: this.mr_totalDistance,
                    mr_allActivitites: JSON.stringify(this.mr_allActivitites),
                    mr_month: this.month
                }
            }).then(() => { 
                this.$route.params.mr_allActivitites = this.mr_allActivitites;
            });
        },

        async checkForPopup() {
            console.log("goal met:", this.goalMet);
            console.log("to prompt:", this.toPrompt);
            console.log("goal:", this.goalWeekly);
            if (this.toPrompt == true) {
                this.showPopup = true;
                if (this.goalMet == true) {
                    this.caseType = 1;
                } else {
                    if (this.goalWeekly == 150) {
                        this.caseType = 3;
                    } else if (this.goalWeekly > 150) {
                        this.caseType = 2;
                    }
                }
            } else {
                console.log("No prompt needed");
            }
        },

        async handleGoalChange(localGoalValue) {
            try {
                console.log("goal change received on home page", localGoalValue);
                const goalResponse = await this.$http.patch("http://127.0.0.1:5011/goal/" + this.goalId, {
                    target: localGoalValue
                })
                console.log(goalResponse);

                const userResponse = await this.$http.patch("http://127.0.0.1:5001/user/id/" + this.userId, {
                    target_minutes: localGoalValue,
                    goal_date: new Date().toISOString().split('T')[0]
                })
                console.log(userResponse);

                this.showPopup = false;
            } catch (error) {
                console.log("error in updating goal:", error);
            }
        },
        getPreviousMonth() {
            const currentDate = new Date();
            let month = currentDate.getMonth();

            if (month === 0) {
                month = 11;
            } else {
                month -= 1;
            }

            // Get the month name from the month index
            const monthNames = ["January", "February", "March", "April", "May", "June", 
                                "July", "August", "September", "October", "November", "December"];
            this.lastMonth = monthNames[month];
        },
    },
    async mounted() {
        try {
            this.fetchUserData();
            this.getPreviousMonth();
            await this.syncNow();
            await this.checkForPopup();
            this.fetchUserData(); // update reflected healthcoins
        } catch (error) {
            console.log("Error during component mount:", error);
        }
    },
}
</script>



<style scoped>
.pageHeader {
    background-color: var(--blue);
    color: var(--default-white)
}

.stickyHeader {
    background-color: var(--grey);
    padding-bottom: 20px;
}

.stickyHeader .displayBlock {
    align-items: center;
    justify-content: center;
}

.container {
    padding: 0 16px 10px 16px;
}

.displayBlock {
    display: flex;
    width: 80%;
    margin: auto;
    padding-top: 16px;
}

.blockLeft, .blockRight {
    flex: 1;
    display: flex;
    flex-direction: column;
    background-color: var(--default-white);
    align-items: center;
    text-align: center;
    padding-top: 15px;
    min-height: 70px;
}

.blockLeft {
    border-right: 1px solid var(--grey-highlight);
    border-radius: 6px 0 0 6px;
}

.blockRight {
    border-radius: 0 6px 6px 0;
}

.blockLeft p, .blockRight p {
    font-family: text-medium;
    font-size: 11px;
    color: var(--default-text);
    margin: 0;
}

.blockText {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.blockText p, .blockText span {
    font-family: text-bold;
    font-size: 17px;
    color: var(--default-text);
    margin: 0;
}

.blockText img, .card .price img {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
}


.pageHeading {
    display: flex;
    align-items: center;
}

.pageHeading img {
    width: 40px;
    height: 40px;
}

.pageHeading p, .headerText .head {
    font-family: text-semibold;
    font-size: 16px;
    color: var(--default-text);
}

.headerText .body {
    font-family: text-medium;
    font-size: 13px;
    color: var(--text-highlight);
}

.updateDetails {
    display: flex;
    justify-content: flex-end;
}

.syncButton {
    font-family: text-medium;
    color: var(--blue);
    font-size: 10px;
    background-color: #E9F3FD;
    border-radius: 5px;
    border: none;
    padding: 8px 10px;
    margin: 0 16px 16px 16px;
}

.basicCard {
    background-color: var(--default-white);
    flex-direction: column;
}

.barLabel {
    padding: 16px 16px 5px 16px;
    color: var(--text-highlight);
    font-size: 13px;
}

.updatedVar {
    font-family: text-bold;
}

.updatedText {
    font-family: text-medium;
}

.bar {
    width: 100%;
    height: auto;
    padding: 5px 16px 16px 16px;
}


.card {
    display: flex;
    flex: 0 0 auto;
    border-radius: 6px;
    border: none;
    width: 165px;
}

.cardImage img {
    width: 165px;
    height: 65px;
    border-radius: 6px 6px 0 0;
}


.lowSlotAlert {
    font-family: text-medium;
    font-size: 8px;
    color: var(--default-white);
    background-color: var(--green);
    border-radius: 5px;
    margin-bottom: 5px;
}

.cardText {
    padding: 16px;
}

.eventName {
    font-family: text-semibold;
    font-size: 12px;
    color: var(--default-text);
    margin: 0;
}

.eventDetails p {
    font-family: text-medium;
    font-size: 10px;
    color: var(--text-highlight);
    margin: 0;
}


</style>