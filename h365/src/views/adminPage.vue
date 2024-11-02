<template>
    <div class="pagePad">
        <h1> Event Attendance </h1>

        <div class="searchAndFilter" style="padding: 0; margin: 0 0 32px 0;">
            <div class="search-bar">
                <i class="uil uil-search"></i>
                <input type="text" v-model="searchInput" @input="searchEvents" placeholder="Search by event name" />
            </div>
        </div>

        <n-collapse v-model:value="expandedEventId" accordion>
            <n-collapse-item
                v-for="event in events"
                :key="event.event_id"
                :name="event.event_id"
                :title="event.title"
                @click="onExpandedEventClick(event.event_id)"
            >
                <n-collapse accordion>
                    <n-collapse-item name="event-details" title="Event Details">
                        <table class="table-spacing">
                            <tr>
                                <td class="label"> Event Mode </td>
                                <td class="value"> {{ event.mode }} </td>
                            </tr>
                            <tr>
                                <td class="label"> Event Location </td>
                                <td class="value"> {{ event.location }} </td>
                            </tr>
                            <tr>
                                <td class="label"> Current Sign-Ups </td>
                                <td class="value"> {{ event.current_signups }} / {{ event.max_signups }} </td>
                            </tr>
                            <tr>
                                <td class="label"> Event Date </td>
                                <td class="value"> {{ event.formattedStartDate }} </td>
                            </tr>
                            <tr>
                                <td class="label"> Event Time </td>
                                <td class="value"> {{ event.formattedStartTime }} - {{ event.formattedEndTime }} </td>
                            </tr>
                        </table>
                    </n-collapse-item>

                    <n-collapse-item name="organiser-details" title="Organiser Details">
                        <table class="table-spacing">
                            <tr>
                                <td class="label"> Event Organiser </td>
                                <td class="value"> {{ event.organiser }} </td>
                            </tr>
                            <tr>
                                <td class="label"> Organiser Email </td>
                                <td class="value"> {{ event.organiser_email }} </td>
                            </tr>
                            <tr>
                                <td class="label"> Organiser Phone Number </td>
                                <td class="value"> {{ event.organiser_phone }} </td>
                            </tr>
                        </table>
                    </n-collapse-item>
                </n-collapse>

                <p style="font-family: text-bold; font-size: 15px; padding-top: 32px; margin-bottom: 5px;"> Participant List </p>

                <table 
                v-if="participants[event.event_id] && participants[event.event_id].length" class="table-spacing"
                style="border: none;">
                    <thead>
                        <tr>
                            <td style="font-family: text-bold; text-decoration: underline; padding-bottom: 0px;"> Name </td>
                            <td style="font-family: text-bold; text-decoration: underline; padding-bottom: 0px;"> Number </td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="participant in participants[event.event_id]" :key="participant.user_event_id">
                            <td>{{ participant.name }}</td>
                            <td>{{ participant.contact_details }}</td>
                            <td>{{ participant.completed }}</td>

                            <td>
                                <n-checkbox
                                    v-model="attendance[event.event_id][participant.user_event_id]"
                                    :checked="participant.completed"
                                    @update:checked="(checked) => handleAttendanceChange(event.event_id, participant, checked)"
                                />
                            </td>
                        </tr>
                    </tbody>
                </table>

                <p v-else> No participants signed up. </p>

            </n-collapse-item>
        </n-collapse>

    </div>

</template>

<script>
import { reactive } from 'vue';

export default {
    data() {
        return {
            allEvents: [],
            events: [],
            participants: reactive({}),
            expandedEventId: null,
            attendance: reactive({}),
            searchInput: "",
        };
    },

    mounted() {
        this.fetchEvents();
    },

    methods: {
        formatDateTime(dateString) {
            const date = new Date(dateString);

            const formattedDate = date.toLocaleDateString("en-GB", {
                day: "2-digit",
                month: "short",
                year: "numeric",
            });

            const formattedTime = date.toLocaleTimeString("en-GB", {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,
            });
            return { formattedDate, formattedTime };
        },

        async fetchEvents() {
            try {
                const response = await this.$http.get("http://127.0.0.1:5002/events");
                // console.log("Fetched events:", response.data);
                this.events = response.data.map(event => {
                    const { formattedDate: formattedStartDate, formattedTime: formattedStartTime } = this.formatDateTime(event.start_date);
                    const { formattedDate: formattedEndDate, formattedTime: formattedEndTime } = this.formatDateTime(event.end_date);
                    return {
                        ...event,
                        formattedStartDate,
                        formattedStartTime,
                        formattedEndDate,
                        formattedEndTime
                    };
                });
                this.allEvents = this.events;
            } catch (error) {
                console.error("Failed to fetch events:", error);
            }
        },

        searchEvents() {
            if (this.searchInput.trim() === "") {
                this.allEvents = this.events;
            } else {
                const keyword = this.searchInput.toLowerCase();
                this.events = this.allEvents.filter(event => 
                    event.title.toLowerCase().includes(keyword)
                );
            }
        },

        async fetchParticipants(eventId) {
            try {
                // console.log(`Fetching participants for event ID: ${eventId}`);
                const response = await this.$http.get(`http://127.0.0.1:5007/userevent/eventusers/${eventId}`);
                if (response.data && response.data.code == 200) {
                    // console.log("Participants data:", response.data.data);
                    this.participants[eventId] = response.data.data;

                    if (!this.attendance[eventId]) {
                        this.attendance[eventId] = {};
                    }
                    response.data.data.forEach(participant => {
                        if (!this.attendance[eventId][participant.user_event_id]) {
                            this.attendance[eventId][participant.user_event_id] = false;
                        }
                    });
                } else {
                    console.warn(`No participants found for event ${eventId}`);
                    this.participants[eventId] = [];
                }
            } catch (error) {
                console.error(`Failed to fetch participants for event ${eventId}:`, error);
                this.participants[eventId] = [];
            }
        },

        onExpandedEventClick(eventId) {
            if (this.expandedEventId === eventId) {
                this.expandedEventId = null;
            } else {
                this.expandedEventId = eventId;
                this.fetchParticipants(eventId);
            }
            // console.log("Expanded Event ID:", this.expandedEventId);
        },


        async handleAttendanceChange(eventId, participant, checked) {
            console.log("Checkbox changed:", checked, "for user_event_id:", participant.user_event_id);
            if (checked && !this.attendance[eventId][participant.user_event_id]) {
                const user_event_ids = [participant.user_event_id];
                const user_ids = [participant.user_id];

                try {
                    await this.$http.post(`http://127.0.0.1:5016/attendance/${eventId}`, {
                        user_event_ids,
                        user_ids
                    });
                    console.log("Attendance recorded successfully for user_event_id:", participant.user_event_id);
                } catch (error) {
                    console.error("Error recording attendance:", error);
                }
            }

            this.attendance[eventId][participant.user_event_id] = checked;

            try {
                await this.$http.patch(`http://127.0.0.1:5007/userevent/${participant.user_event_id}`, {
                    completed: checked
                });
                console.log("Attendance updated successfully for user_event_id:", participant.user_event_id);

                this.fetchParticipants(eventId);
            } catch (error) {
                console.error("Error updating attendance status:", error);
            }
        }
    },

    watch: {
        expandedEventId(newVal) {
            console.log("expandedEventId changed:", newVal);
            if (newVal) {
                this.fetchParticipants(newVal);
            }
        }
    },

}
</script>

<style scoped>
h1 {
    font-family: text-bold;
    font-size: 25px;
    padding-bottom: 16px;
}

.pagePad {
    padding: 32px;
}

.search-bar {
    width: 100%;
}

.display-flex {
    display: flex;
    justify-content: space-between;
}

table {
    border: 1px solid #EBEBE9;
    width: 100%;
}

.table-spacing {
    margin-bottom: 10px;
}

td {
    padding: 10px;
}

.label, .value {
    font-family: text-bold;
    font-size: 10px;
    color: var(--text-highlight);
    border: 1px solid #EBEBE9;
    text-align: center;
}

.label {
    background-color: var(--default-white);
}

/* .n-collapse {
    --n-font-size: 12px;
    --n-title-padding: 5px 0 0 0;
} */

/* <div class="n-collapse" style="--n-font-size: 14px; --n-bezier: cubic-bezier(.4, 0, .2, 1); 
--n-text-color: rgb(51, 54, 57); --n-divider-color: rgb(239, 239, 245); --n-title-padding: 16px 0 0 0; 
--n-title-font-size: 14px; --n-title-text-color: rgb(31, 34, 37); --n-title-text-color-disabled: rgba(194, 194, 194, 1); 
--n-title-font-weight: 400; --n-arrow-color: rgb(51, 54, 57); --n-arrow-color-disabled: rgba(194, 194, 194, 1); 
--n-item-margin: 16px 0 0 0;"> */


</style>