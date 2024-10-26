<template>
    <div class="stickyHeader">
        <div class="pageHeader">
            <i class="uil uil-angle-left" @click="goBack"></i>
            <p> New Trade Request </p>
        </div>
    </div>

    <div class="pagePad">
        <n-space vertical class="trade-request-container">
            <n-steps :current="stepState.currentStep" :status="stepState.currentStatus">
                <n-step title="Select Trade" />
                <n-step title="Select Yours" />
                <n-step title="Confirmation" />
            </n-steps>
        </n-space>

        <div class="subtext">
            <p v-if="currentStep == 1"> Select a collectible you want. </p>
            <p v-if="currentStep == 2"> Select a collectible to give away. </p>
            <p v-if="currentStep == 3"> Your trade request: </p>
        </div>

        <div class="search-bar" v-if="currentStep == 1 || currentStep == 2">
            <i class="uil uil-search"></i>
            <input type="text" v-model="searchInput" @input="searchTrades" placeholder="Search by card, set, or user" />
        </div>
    </div>

        <div class="step-content">
            <div v-if="stepState.currentStep === 1">
                <selectTrade @card-selected="handleCardWant" @next="nextStep" />
            </div>

            <div v-if="stepState.currentStep === 2">
                <selectYours @card-selected="handleCardGive" @back="previousStep" @next="nextStep" />
            </div>

            <div v-if="stepState.currentStep === 3">
                
                <div class="pagePad">
                    <div class="overall-card drop-shadow">
                        <div class="offer">
                            <div class="card">
                                <p class="head">Offering Up</p>
                                <img :src="getImageSrc(cardGiveSet, cardGiveTitle)">
                                <p class="cardName">{{ cardGiveTitle }}</p>
                                <p class="cardSet">{{ cardGiveSet }}</p>
                            </div>
                        </div>

                        <i class="uil uil-exchange"></i>

                        <div class="receive">
                            <div class="card">
                                <p class="head">Requesting For</p>
                                <img :src="getImageSrc(cardWantSet, cardWantTitle)">
                                <p class="cardName">{{ cardWantTitle }}</p>
                                <p class="cardSet">{{ cardWantSet }}</p>
                            </div>
                        </div>

                    </div>
                </div>

                <div class="bookNowContainer">
                    <button @click="back" class="backButton"> Back </button>
                    <button @click="next" class="nextButton"> Confirm </button>
                </div>

            </div>

        </div>

</template>

<script>
import { defineComponent, reactive } from "vue";
import selectTrade from '../components/selectTrade.vue';
import selectYours from '../components/selectYours.vue';

export default defineComponent({
    components: {
        selectTrade,
        selectYours,
    },

    data() {
        return {
            searchInput: '',
            searchResults: {},
            steps: ["Select Trade", "Select Yours", "Confirmation"],
            cardWant: null,
            cardGive: null,
            cardWantTitle: '',
            cardGiveTitle: '',
            cardWantSet: '',
            cardGiveSet: '',
        };
    },

    setup() {
        const stepState = reactive({
            currentStep: 1,
            currentStatus: "process"
        });

        function next() {
            if (stepState.currentStep < 3) {
                stepState.currentStep++;
            }
        }

        function prev() {
            if (stepState.currentStep > 1) {
                stepState.currentStep--;
            }
        }

        return {
            stepState,
            next,
            prev
        };
    },

    methods: {
        goBack() {
            this.$router.go(-1);
        },

        searchCards() {
            this.searchResults = {};

            if (this.searchInput) {
                const lowerCaseInput = this.searchInput.toLowerCase();
                for (let type in this.allCards) {
                    if (type.toLowerCase().includes(lowerCaseInput)) {
                        this.searchResults[type] = this.allCards[type];
                    } else {
                        const card_set = this.allCards[type];
                        for (let card of card_set) {
                            if (card.title.toLowerCase().includes(lowerCaseInput)) {
                                if (!this.searchResults[type]) {
                                    this.searchResults[type] = [];
                                }
                                this.searchResults[type].push(card);
                            }
                        }
                    }
                }
            }
        },

        handleCardWant(card) {
            this.cardWant = card;
            this.cardWantTitle = card.title;
            this.cardWantSet = card.card_type;
        },

        handleCardGive(card) {
            this.cardGive = card;
            this.cardGiveTitle = card.title;
            this.cardGiveSet = card.card_type;
        },

        nextStep() {
            if (this.stepState.currentStep < 3) {
                this.stepState.currentStep++;
            }
        },

        previousStep() {
            if (this.stepState.currentStep > 1) {
                this.stepState.currentStep--;
            }
        },

        confirmTrade() {
            if (this.cardWant && this.cardGive) {
                console.log("Confirming trade:", this.cardWant, this.cardGive);
                alert("Trade confirmed!");
            } else {
                alert("Error: Cards are missing!");
            }
        },
    
        async fetchCardTitles() {
            if (this.cardWant && this.cardGive) {
                try {
                    const wantResponse = await this.$http.get(`http://127.0.0.1:5003/card/${this.cardWant.card_id}`);
                    const giveResponse = await this.$http.get(`http://127.0.0.1:5003/card/${this.cardGive.card_id}`);

                    this.cardWantTitle = wantResponse.data.data.title;
                    this.cardGiveTitle = giveResponse.data.data.title;
                    this.cardWantSet = wantResponse.data.data.card_type;
                    this.cardGiveSet = giveResponse.data.data.card_type;
                } catch (error) {
                    console.error("Error fetching card titles:", error);
                }
            }
        },

        getImageSrc(set, title) {
            return require(`@/assets/icons/collection/${set.toLowerCase().replace(/\s+/g, "_")}/${title.toLowerCase()}.png`);
        },
    },

    computed: {
        filteredCardsData() {
            return Object.keys(this.searchResults).length > 0 && this.searchInput
                ? this.searchResults
                : this.allCards;
        }
    }
});
</script>

<style>
.pageHeader {
    background-color: var(--purple);
    color: var(--default-white);
}

.pagePad {
    padding: 0 32px;
}

.n-space {
    padding: 32px 0;
}

.n-step {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.trade-request-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.n-step-content-header__title {
    font-family: text-medium;
    font-size: 12px;
    color: var(--text-highlight);
    text-align: center;
}

.subtext {
    font-family: text-medium;
    font-size: 13px;
    color: var(--text-highlight);
}

div .search-bar {
    width: 100%;
    display: flex;
    justify-content: center;
}

.overall-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: var(--default-white);
    padding: 26px;
    border-radius: 6px;
}

.card {
    border: none;
}

i {
    font-size: 30px;
}

.head, .cardName, .cardSet {
    font-family: text-bold;
    margin: 0;
    text-align: center;
}

.head {
    font-size: 15px;
    color: var(--default-text);
}

.cardName {
    font-size: 12px;
    color: var(--default-text);
}

.cardSet {
    font-size: 12px;
    color: var(--orange);
}

.card img {
    width: 100%;
    max-width: 120px;
    height: auto;
    display: flex;
    margin: auto;
}

.bookNowContainer {
    z-index: 10;
    width: 100%;
    display: flex;
    justify-content: space-between;
    position: fixed;
    bottom: 0px;
    border: none;
}

.backButton, .nextButton {
    width: 50%;
    padding: 25px 0px;
    border: none;
    text-align: center;
    font-family: text-medium;
    font-size: 13px;
}

.backButton {
    background-color: var(--default-white);
    color: var(--blue);
}

.nextButton {
    background-color: var(--blue);
    color: var(--grey);
}

</style>