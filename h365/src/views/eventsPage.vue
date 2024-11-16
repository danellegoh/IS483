<template>
    <div>
        <div class="stickyHeader">
            <div class="pageHeader">
                <p>Events</p>
            </div>
            <n-tabs v-model:value="selectedTab" type="line" class="pageTab">
                <n-tab name="allEvents">
                    All
                </n-tab>
                <n-tab name="bookedEvents">
                    Booked
                </n-tab>
            </n-tabs>
        </div>

        <div class="pagePad">
            <div class="searchAndFilter" style="padding: 0;">
                <div class="search-bar">
                    <i class="uil uil-search"></i>
                    <input type="text" v-model="searchInput" @input="searchEvents" placeholder="Search by event or location" />
                </div>
                <div class="filterButton">
                    <datePicker v-model="dateInput" @update:modelValue="searchEvents"/>
                </div>
            </div>

            <!-- Check if there are no filtered events or eventData -->
            <div v-if="isEmpty(filteredEventsData)">
                <p class="no-events-found">No matching events found</p>
            </div>

            <!-- loop for each date -->
            <div v-for="date in sortedDates" :key="date">

                <!-- date header -->
                <div class="basicHeader">
                    <p style="padding-top: 16px; padding-bottom: 0; margin-bottom: 10px;"> {{ formattedDateHeader(date) }} </p>
                </div>
                
                <!-- recommended events -->
                <div v-if="recommendedEvents[date] && recommendedEvents[date].length">

                <!-- recommended header -->
                <div class="pageHeading">
                    <img src="../assets/icons/events/star.png">
                    <p style="font-family: text-semibold; font-size: 16px;"> Recommended for you </p>
                </div>

                <!-- recommended events cards -->
                <div v-for="event in recommendedEvents[date]" :key="event.event_id">
                    <router-link :to="{ name: 'viewEventPage', params: { eventId: event.event_id } }">
                        <div class="basicCard">
                            <div class="cardImage">
                                <img class="eventImage" 
                                    :src="getEventImage(event.title)" 
                                >
                            </div>

                            <div class="cardText">

                                <!-- v-if few slots left -->
                                <div class="lowSlotAlert" v-if="event.max_signups - event.current_signups <= 5">
                                    Few Slots Left
                                </div>

                                <!-- programme name -->
                                <p class="programmeName" v-if="event.event_program != 'Null'"> {{ event.event_program }} </p>

                                <!-- activity name -->
                                <p class="eventName">{{ event.title }}</p>

                                <!-- date, day, and time  -->
                                <div class="eventInfo1">
                                    <i class="uil uil-schedule eventIcon"></i>
                                    <div class=eventDetails>
                                        <p>{{ formattedDate(event.start_date) }}</p>
                                        <p>{{ formattedTime(event.start_date, event.end_date) }}</p>
                                    </div>
                                </div>

                                <!-- location -->
                                <div class="eventInfo2"
                                    :style="{ marginBottom: recommendedEvents[date] && recommendedEvents[date].length ? '10px' : '30px' }"
                                >
                                    <i class="uil uil-map-pin eventIcon"></i>
                                    <div class=eventDetails>
                                        <p>{{ event.location }}</p>
                                    </div>
                                </div>
                                <div class="eventBtnIntensity">
                                    <form action="">
                                        <button class="bookEventBtn">Book Now</button>
                                    </form>

                                    <!-- intensity -->
                                    <div class="intensity">
                                        <p>Intensity: </p>
                                        <img v-if="event.tier === 1" src="../assets/icons/events/intensity1.png">
                                        <img v-else-if="event.tier === 2" src="../assets/icons/events/intensity2.png">
                                        <img v-else-if="event.tier === 3" src="../assets/icons/events/intensity3.png">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </router-link>
                </div>

                <br>
                </div>
                
                <!-- all events header -->
                <div class="pageHeading">
                    <img src="../assets/icons/events/folder.png">
                    <p style="font-family: text-semibold; font-size: 16px;">All Events</p>
                </div>

                <!-- all events cards -->
                <div v-for="event in filteredEventsData[date]" :key="event.event_id">
                    <router-link :to="{ name: 'viewEventPage', params: { eventId: event.event_id } }">
                        <div class="basicCard">
                            <div class="cardImage">
                                <img class="eventImage"
                                    :src="getEventImage(event.title)" 
                                >
                            </div>

                            <div class="cardText">
                                <!-- v-if few slots left -->
                                <div class="lowSlotAlert" v-if="event.max_signups - event.current_signups <= 5">
                                    Few Slots Left
                                </div>

                                <!-- programme name -->
                                <p class="programmeName" v-if="event.event_program != 'Null'">
                                    {{ event.event_program }}
                                </p>

                                <!-- activity name -->
                                <p class="eventName">
                                    {{ event.title }}
                                </p>

                                <!-- date, day, and time  -->
                                <div class="eventInfo1">
                                    <i class="uil uil-schedule eventIcon"></i>
                                    <div class=eventDetails>
                                        <p>{{ formattedDate(event.start_date) }}</p>
                                        <p>{{ formattedTime(event.start_date, event.end_date) }}</p>
                                    </div>
                                </div>

                                <!-- location -->
                                <div class="eventInfo2" 
                                    :style="{ marginBottom: recommendedEvents[date] && recommendedEvents[date].length ? '10px' : '30px' }"
                                >
                                    <i class="uil uil-map-pin eventIcon"></i>
                                    <div class=eventDetails>
                                        <p>{{ event.location }}</p>
                                    </div>
                                </div>

                                <div class="eventBtnIntensity">
                                    <button class="bookEventBtn">Book Now</button>

                                    <!-- intensity -->
                                    <div class="intensity">
                                        <p>Intensity: </p>
                                        <img v-if="event.tier === 1" src="../assets/icons/events/intensity1.png">
                                        <img v-else-if="event.tier === 2" src="../assets/icons/events/intensity2.png">
                                        <img v-else-if="event.tier === 3" src="../assets/icons/events/intensity3.png">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </router-link>
                </div>
                
            </div>
        </div>
    </div>

</template>

<style scoped>

.stickyHeader {
    top: 0;
}

.basicHeader {
    text-align: left;
    font-family: text-bold;
    border-bottom: 1px solid rgba(123, 120, 116, 1);
}

.pageHeader {
    background-color: var(--yellow);
}

.pageTab {
    background-color: var(--grey);
}

.basicCard {
    width: 90%;
    display: flex;
    background-color: var(--default-white);
    margin: 0 auto;
    margin-bottom: 20px;
}

.basicCard .cardImage, .basicCard .cardText {
    flex: 1;
}

.basicCard .cardImage {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding: 0px;
}

.basicCard .cardImage img {
    height: 100%;
    width: 100%;
    object-fit: contain;
    margin: 0px;
}

.basicCard .cardText {
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.cardText {
    max-height: 199px;
}

.lowSlotAlert {
    font-family: text-medium;
    font-size: 8px;
    color: var(--default-white);
    background-color: var(--red);
    margin-bottom: 4px;
}

.programmeName {
    font-family: text-medium;
    font-size: 10px;
    color: var(--text-highlight);
    margin-bottom: 4px;
}

.eventName {
    font-family: text-bold;
    font-size: 16px;
    color: var(--default-text);
    margin-bottom: 10px;
    line-height: 16px;
}

.eventIcon {
    color: var(--text-highlight);
}

.eventInfo1 {
    display: flex;
    padding: 0px;
    margin-bottom: 0px;
    align-items: center;
    justify-content: flex-start;
}

.eventInfo2 {
    display: flex;
    padding: 0px;
    margin-bottom: 10px;
    align-items: center;
    justify-content: flex-start;
}

.eventDetails {
    font-family: text-semibold;
    color: var(--text-highlight);
    font-size: 9px;
    padding-left: 10px;
    line-height: 10px;
}

.eventDetails p {
    margin-bottom: 0px;
}

.bookEventBtn {
    font-family: text-medium;
    color: var(--grey);
    font-size: 10px;
    background-color: var(--blue);
    border-radius: 5px;
    border: none;
    padding: 4px 8px;
}

.eventBtnIntensity {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.eventBtnIntensity .intensity {
    display: flex;
    align-items: center;
}

.eventBtnIntensity .intensity img {
    margin-left: 3px;
}

.intensity p {
    font-family: text-semibold;
    font-size: 9px;
    color: var(--text-highlight);
    margin: 5px 5px 0 0;
}

.no-events-found {
    text-align: center;
    font-family: text-semibold;
    color: var(--text-highlight);
    font-size: 14px;
    margin-top: 20px;
}

.eventImage {
    border-radius: 5px 0 0 5px;
}

</style>

<script>
import { defineComponent, ref, watch, computed } from "vue";
import { useRouter } from 'vue-router';
import datePicker from '../components/datePicker.vue';
import { useStore } from 'vuex';
import axios from 'axios';

const apiBaseURL = process.env.VUE_APP_API_BASE_URL;

export default defineComponent({
    components: {
        datePicker
    },
    setup() {
        console.log("all events page");
        const selectedTab = ref('allEvents');
        const router = useRouter();

        const store = useStore();
        const userId = computed(() => store.state.userId);

        watch(selectedTab, (newTab) => {
            if (newTab === 'allEvents') {
                router.push({ path: '/events' });
            } else if (newTab === 'bookedEvents') {
                router.push({ path: '/booked' });
            }
        });

        return {
            selectedTab,
            userId
        };
    },
    async mounted() {
        this.fetchEvents();
        if (this.userId) {
            await this.fetchRecommendedEvents();
        }
    },
    data() {
        return {
            searchInput: "",
            dateInput: null,
            sortedDates: [],
            eventData: {},
            recommendedEvents: {},
            filteredEvents: null
        };
    },
    methods: {
        async fetchEvents() {
            try {
                // const response = await axios.get("http://127.0.0.1:5002/event/available");
                const response = await axios.get(`${apiBaseURL}/event/available`);
                const eventDataResponse = response.data.data;
                this.eventData = {};
                this.sortedDates = [];
                for (const event of eventDataResponse) {
                    const date_key = event.start_date.split("T")[0];
                    if (!this.eventData[date_key]) {
                        this.eventData[date_key] = [];
                        this.sortedDates.push(date_key);
                    }
                    this.eventData[date_key].push(event);
                }
                this.sortedDates.sort();
                console.log(this.eventData);
            } catch (error) {
                console.error("Error fetching events:", error);
            }
        },
        async fetchRecommendedEvents() {
            try {
                // const response = await axios.get(`http://localhost:5042/user/${this.userId}/eligible-events`)
                const response = await axios.get(`${apiBaseURL}/user/${this.userId}/eligible-events`);
                if (response.data.code === 200) {
                    const eventIds = response.data.data;
                    // const eventDetailsPromises = eventIds.map(id =>
                    //     axios.get(`http://localhost:5002/event/${id}`)
                    // );
                    const eventDetailsPromises = eventIds.map(id =>
                        axios.get(`${apiBaseURL}/event/${id}`)
                    );
                    const eventDetailsResponses = await Promise.all(eventDetailsPromises);
                    
                    this.recommendedEvents = {};

                    for (const res of eventDetailsResponses) {
                        const event = res.data.data;
                        const date_key = event.start_date.split("T")[0];
                        if (!this.recommendedEvents[date_key]) {
                            this.recommendedEvents[date_key] = [];
                        }
                        this.recommendedEvents[date_key].push(event);
                    }
                } else {
                    console.error("Failed to fetch recommended events:", response.data.error);
                }
            } catch (error) {
                console.error("Error fetching recommended events:", error);
            }
        },
        formattedDate(dateStr) {
            const date = new Date(dateStr);
            const day = date.getDate();
            const month = new Intl.DateTimeFormat('en-US', { month: 'short' }).format(date);
            const year = date.getFullYear();
            const weekday = new Intl.DateTimeFormat('en-US', { weekday: 'short' }).format(date);
            return `${day} ${month} ${year}, ${weekday}`;
        },
        formattedDateHeader(dateStr) {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            });
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
        async searchEvents() {
            // const url = "http://127.0.0.1:5002/event/search";
            const url = `${apiBaseURL}/event/search`;
            const params = {};
            if (this.searchInput) params.search_input = this.searchInput;
            if (this.dateInput) params.date_input = this.dateInput.split("T")[0];

            try {
                const response = await axios.get(url, { params });
                if (response.status === 200) {
                    const responseData = response.data.data;
                    this.filteredEvents = {};
                    this.sortedDates = [];
                    for (const event of responseData) {
                        const date_key = event.start_date.split("T")[0];
                        if (!this.filteredEvents[date_key]) {
                            this.filteredEvents[date_key] = [];
                            this.sortedDates.push(date_key);
                        }
                        this.filteredEvents[date_key].push(event);
                    }
                }
            } catch (error) {
                console.log("Error during search:", error);
                this.filteredEvents = null;
                this.sortedDates = [];
            }
        },
        getEventImage(programName) {
            switch (programName) {
                case 'Move It':
                    return require('../assets/icons/events/event1.png');
                case 'Family Fitness':
                    return require('../assets/icons/events/event2.png');
                case 'Shop, Cook, Eat Healthy':
                    return require('../assets/icons/events/event3.png');
                case 'Mall Workouts':
                    return require('../assets/icons/events/event4.png');
                case 'Step Up Challenge':
                    return require('../assets/icons/events/event5.png');
                default:
                    return require('../assets/icons/events/event1.png');
            }
        },
        isEmpty(eventsData) {
            return !eventsData || Object.keys(eventsData).length === 0;
        }
    },

    computed: {
        filteredEventsData() {
            return this.searchInput || this.dateInput ? this.filteredEvents || {} : this.eventData;
        }
    }
});
</script>