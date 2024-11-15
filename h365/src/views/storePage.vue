<template>
    <div class="stickyHeader">
        <div class="pageHeader">
            <p> Store </p>
        </div>

        <div class="displayBlock">
            <div class="blockLeft">
                <div class="blockText">
                    <p style="margin-right: 5px"> {{ numHealthCoins }} </p>
                    <span> <img src="../assets/icons/collection/coin.png"> </span>
                </div>
                <p> My Healthcoins </p>
            </div>

            <router-link :to="{ name: 'allCardsPage'}" class="router-link-custom">
                <div class="blockRight">
                    <div class="blockText">
                        <img src="../assets/icons/collection/lock.png" style="margin-right: 5px;">
                        <p> <span> {{ numUnlocked }} </span> / {{ numCards }} </p>
                    </div>
                    <p> Collectibles Unlocked ➔ </p>
                </div>
            </router-link>
        </div>
    </div>

    <div class="pagePad" style="padding-bottom: 5px;">
        <div class="limited up">
            <p> 🔥 GET IT BEFORE IT'S GONE 🔥 </p>

            <div class="countdown">
                <vue3-flip-countdown
                    v-if="formattedDeadline"
                    :deadline="formattedDeadline"
                    mainColor="#ff774d"
                    mainFlipBackgroundColor="#F5F4F1"
                    secondFlipBackgroundColor="#F5F4F1"
                    labelColor="#F5F4F1"
                    countdownSize="2.0rem"
                    labelSize="0.8rem"
                />
            </div>

            <div class="shopltd">
                <button @click="isOpen = !isOpen" class="shopNowBtn"> 
                    Shop Now!
                </button>
            </div>

        </div>

        <div v-show="isOpen" class="limited down">
            <div v-for="(cards, cardType) in limitedEditionCards" :key="cardType" class="set">
                <div class="set" style="padding: 0;">
                    <p> {{ cardType }} </p>
                    <div class="carousel">
                        <div v-for="card in cards" :key="card.card_id">
                            <div :class="['card', 'drop-shadow', { 'card-owned': userCards.includes(card.card_id) }]">
                                <p class="cardName"> {{ card.title }} </p>
                                <img :src="getCardImage(card.title, card.collection_id)" />
                                <div class="price">
                                    <img src="../assets/icons/collection/coin.png" style="margin-right: 5px;">
                                    <p> {{ card.points_required }} </p>
                                </div>
                                <button
                                    v-if="userCards.includes(card.card_id)"
                                    class="viewCardBtn" @click="openInfoPopup(card.card_id, card.description, card.recommendation)"> View 
                                </button>
                                <button
                                    v-else
                                    class="bookEventBtn" @click="openUnlockPopup(card.title, card.points_required, card.card_id)"> Unlock 
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>

    <div class="container">
        <div class="info">
            Redeem your HealthCoins for exclusive digital collectibles and showcase them on your profile.
        </div>
    </div>

    <div class="pagePad">
        <div class="search-bar">
            <i class="uil uil-search"></i>
            <input type="text" v-model="searchInput" @input="searchCards" placeholder="Search by card or set" />
        </div>

        <div class="head">
            <p> Explore Sets </p>
            <router-link :to="{ name: 'tradePage'}">
                <button class="tradeButton">
                    <label> Trade </label>
                    <i class="uil uil-exchange"> </i>
                </button>
            </router-link>
        </div>

        <div v-for="(cards, cardType) in filteredCardsData" :key="cardType" class="set">
            <div class="set">
                <p> {{ cardType }} </p>
                <div class="carousel">
                    <div v-for="card in cards" :key="card.card_id">
                        <div :class="['card', { 'card-owned': userCards.includes(card.card_id) }]">
                            <p class="cardName"> {{ card.title }} </p>

                            <img :src="getCardImage(card.title, card.collection_id)" />

                            <div class="price">
                                <img src="../assets/icons/collection/coin.png" style="margin-right: 5px;">
                                <p> {{ card.points_required }} </p>
                            </div>

                            <button
                                v-if="userCards.includes(card.card_id)"
                                class="viewCardBtn" @click="openInfoPopup(card.card_id, card.description, card.recommendation)"> View 
                            </button>

                            <button
                                v-else
                                class="bookEventBtn" @click="openUnlockPopup(card.title, card.points_required, card.card_id)"> Unlock 
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <Popup
        v-if="isPopupVisible"
        :visible="isPopupVisible"
        :type="popupType"
        :cardName="cardName"
        :cardPrice="cardPrice"
        :cardId="cardId"
        :errorMessage="errorMessage"
        :cardDescription="cardDesc"
        :cardRecommendation="cardRec"
        @close="closePopup"
        @unlock-card="unlockCard"
    />

</template>

<script>
import Popup from '@/components/popUp.vue';
import { useStore } from 'vuex';
import { computed } from 'vue';

export default {
    components: {
        Popup,
    },

    data() {
        return {
            isPopupVisible: false,
            cardName: '',
            cardPrice: 0,
            cardId: '',
            cardDesc: '',
            cardRec: '',
            popupType: '',
            numHealthCoins: 0,
            numUnlocked: 0,
            numCards: 0,

            allCards: {},
            limitedEditionCards: {},
            userCards: [],

            errorMessage: '',
            searchInput: '',
            searchResults: {},
            collectionDataById: {},

            expiryDate: "",
            isOpen: false,
        };
    },
    methods: {
        openUnlockPopup(cardName, cardPrice, cardId) {
            this.cardName = cardName;
            this.cardPrice = cardPrice;
            this.cardId = cardId;
            this.popupType = 'unlock';
            this.isPopupVisible = true;
        },

        closePopup() {
            this.isPopupVisible = false;
            this.errorMessage = ''; 
        },

        openInfoPopup(cardId, cardDesc, cardRec) {
            this.cardId = cardId;
            this.cardDesc = cardDesc;
            this.cardRec = cardRec;
            this.popupType = 'info';
            this.isPopupVisible = true;
        },

        async unlockCard(cardId) {
            // console.log("unlocking card with ID:", cardId);

            try {
                const response = await this.$http.post("http://127.0.0.1:5006/usercard/buy", {
                    user_id: this.userId,
                    card_id: cardId
                })
                console.log(response);
                // console.log("unlock card successful");

                // refresh user cards and points
                await this.fetchUserData();
                await this.fetchUserCards();

                this.isPopupVisible = false;
            }
            catch (error) {
                // console.log("Unlock Card:", error);
                let responseError = error.response.data.error;
                // console.log(responseError);
                if (responseError == "Insufficient HealthCoins to buy this card") {
                    this.errorMessage = "Insufficient HealthCoins to buy this card";
                }
                else {
                    this.errorMessage = "Failed to join the event. Please try again.";
                }  
            }
        },

        // Fetch user data
        async fetchUserData() {
            try {
                const userReponse = await this.$http.get("http://127.0.0.1:5001/user/" + this.userEmail);
                const userData = userReponse.data.data;
                this.numHealthCoins = userData["total_point"];
            } catch (error) {
                console.error("Error fetching user data:", error);
            }
        },

        // Fetch user cards
        async fetchUserCards() {
            try {
                const userCardResponse = await this.$http.get("http://127.0.0.1:5006/usercard/user/" + this.userId);
                const userCardData = userCardResponse.data.data;
                
                this.userCards = userCardData["cards"].map(card => card["card_id"]);
                this.numUnlocked = userCardData["count_redeemed"];
            } catch (error) {
                console.error("Error fetching user cards:", error);
            }
        },

        // fetch all cards for store and separate based on "limited edt" or "normal"
        async fetchAllCards() {
            const collectionResponse = await this.$http.get("http://127.0.0.1:5022/collections");
            const collectionData = collectionResponse.data.data;
            for (let i = 0; i < collectionData.length; i++) {
                this.collectionDataById[collectionData[i]["collection_id"]] = {
                    "card_type": collectionData[i]["collection_name"], 
                    "expired": collectionData[i]["expired"] // datetime
                }
            }
            // console.log("haha", this.collectionDataById);

            const cardReponse = await this.$http.get("http://127.0.0.1:5003/cards");
            const cardData = cardReponse.data;
            const now = new Date();

            for (let i = 0; i < cardData.length; i++) {
                if (cardData[i]["event_id"] == null) {
                    let collection_id = cardData[i]["collection_id"];
                    let card_type = this.collectionDataById[collection_id]["card_type"];
                    let expired = this.collectionDataById[collection_id]["expired"];
                    const expiredDate = expired ? new Date(expired) : null;
                    // console.log("haha", card_type, expired);

                    if (expiredDate == null) {
                        if (!this.allCards[card_type]) {
                            this.allCards[card_type] = [];
                        }
                        this.allCards[card_type].push(cardData[i]);
                    } else if (expiredDate >= now) {
                        if (!this.limitedEditionCards[card_type]) {
                            this.limitedEditionCards[card_type] = [];
                        }
                        this.limitedEditionCards[card_type].push(cardData[i]);
                        
                        if (expiredDate > now && (!this.expiryDate || expiredDate < new Date(this.expiryDate))) {
                            this.expiryDate = this.formatDateToString(expiredDate);
                        }
                    }
                }
            }
            console.log(this.expiryDate);
            // console.log(typeof this.expiryDate)
            // console.log("normal cards", this.allCards);
            // console.log("limited edition cards", this.limitedEditionCards);
            // console.log("checking all cards from fetch all", this.allCards);
            this.numCards = cardData.length;
        },

        formatDateToString(dateString) {
            const date = new Date(dateString);

            if (isNaN(date.getTime())) {
                console.error(`Invalid date format: ${dateString}`);
                return '';
            }

            const year = date.getUTCFullYear();
            const month = String(date.getUTCMonth() + 1).padStart(2, '0');
            const day = String(date.getUTCDate()).padStart(2, '0');
            const hours = String(date.getUTCHours()).padStart(2, '0');
            const minutes = String(date.getUTCMinutes()).padStart(2, '0');
            const seconds = String(date.getUTCSeconds()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },


        getCardImage(card_title, card_collection_id) {
            // console.log("check collection id:", card_collection_id);
            if (!card_title || !card_collection_id) {
                console.error("Invalid card_title or card_collection_id:", card_title, card_collection_id);
                return ;
            }

            const formattedTitle = card_title.toLowerCase().replace(/\s+/g, "_");
            // console.log(formattedTitle);
            const card_set = this.collectionDataById[card_collection_id]["card_type"]
            const formattedSetName = card_set.toLowerCase().replace(/\s+/g, "_");
            return require(`@/assets/icons/collection/${formattedSetName}/${formattedTitle}.png`);
        },

        searchCards() {
            this.searchResults = {};

            if (this.searchInput) {
                var lowerCaseInput = this.searchInput.toLowerCase();

                for (let type in this.allCards) {
                    console.log("checking type in search", type);
                    if (type.toLowerCase().includes(lowerCaseInput)) {
                        this.searchResults[type] = this.allCards[type];
                    } else {
                        // console.log(this.allCards[type]);
                        var card_set = this.allCards[type];
                        // console.log("card set check", card_set);
                        for (let i = 0; i < card_set.length; i++) {
                            let card = card_set[i];
                            // console.log("card", card);
                            if (card.title.toLowerCase().includes(lowerCaseInput)) {
                                // console.log("title check pass", card.title);
                                if (!this.searchResults[type]) {
                                    this.searchResults[type] = [];
                                }
                                this.searchResults[type].push(card);
                            }
                        }
                    }
                }
                // console.log("search results check", this.searchResults);
                
            } else {
                this.searchResults = {};
            }
        },

        getCountdownTarget(expiryDate) {
            return expiryDate ? new Date(expiryDate).getTime() : null;
        },
    },
    setup() {
        // console.log("store page");
        const store = useStore();
        const userId = computed(() => store.state.userId);
        const userEmail = computed(() => store.state.userEmail)
        
        console.log(userEmail.value);
        
        return {
            userId,
            userEmail
        };
    },
    async mounted() {
        try {
            this.fetchUserData();
            this.fetchAllCards();
            this.fetchUserCards(); 
            console.log(this.allCards);
        }
        catch (error) {
            console.log("error:", error);
            this.numUnlocked = 0;
            
        }
    },
    computed: {
        filteredCardsData() {
            return Object.keys(this.searchResults).length > 0 && this.searchInput
            ? this.searchResults
            : this.allCards;
        },

        formattedDeadline() {
            return this.expiryDate ? this.expiryDate : null;
        }
    }
};
</script>

<style scoped>
.pageHeader {
    background-color: var(--orange);
    color: var(--default-white)
}

.stickyHeader {
    background-color: var(--grey);
    padding-bottom: 16px;
}

.stickyHeader .displayBlock {
    align-items: center;
    justify-content: center;
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

.info {
    font-family: text-regular;
    font-size: 13px;
    color: var(--default-text);
    text-align: center;
    padding: 16px 0 20px 0;
}

div .search-bar {
    width: 100%;
    display: flex;
    justify-content: center;
}

.pagePad {
    padding: 0 32px;
    padding-bottom: 60px;
}

.head {
    display: flex;
    justify-content: space-between;
    padding: 30px 0 0 0;
}

.head p, .set p {
    margin: 0;
    font-family: text-bold;
    font-size: 16px;
    color: var(--default-text);
}

.set p {
    color: var(--text-highlight);
}

.set {
    padding-bottom: 16px;
}

button {
    all: unset;
    padding: 11px 24px;
    border-radius: 6px;
    color: var(--default-white);
}

button label {
    margin-right: 5px;
}

.tradeButton {
    background: linear-gradient(180deg, #814FF0, #462D7F);
}

.card {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    padding: 16px 0;
    border-radius: 10px;
    border: none;
    width: 130px;
}

.cardName {
    font-family: text-bold;
    font-size: 12px;
    color: var(--default-text);
    text-align: center;
    margin-bottom: 0;
}

.card img {
    width: 65px;
    height: auto;
    margin: 5px 0 0 0;
}

.price {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 5px 0;
}

.price img {
    margin: 0;
}

.price p {
    font-family: text-bold;
    font-size: 12px;
    color: var(--text-highlight);
    margin-bottom: 0;
}

.card .bookEventBtn {
    font-family: text-medium;
    color: var(--grey);
    font-size: 10px;
    background-color: var(--green);
    border-radius: 5px;
    border: none;
    padding: 5px 10px;
    width: 85px;
    text-align: center;
}

.card .viewCardBtn {
    font-family: text-medium;
    color: var(--grey);
    font-size: 10px;
    background-color: var(--blue);
    border-radius: 5px;
    border: none;
    padding: 5px 10px;
    width: 85px;
    text-align: center;
}

.card-owned {
    background-color: #D8D8D5;
}

.limited {
    width: 100%;
    background-color: var(--default-white);
    padding: 16px;
}

.limited p {
    font-family: text-bold;
    text-align: center;
}

.up {
    border-radius: 6px;
    background: linear-gradient(180deg, #114ada, #097BEE);
    color: var(--default-white);
    margin-top: 16px;
}

.down {
    border-radius: 0 0 6px 6px;
}

.countdown {
    width: 100%
}

.set {
    padding: 0;
}

.shopNowBtn {
    background-color: var(--red);
    color: #fff;
    border: none;
    padding: 5px 10px;
    font-size: 10px;
    cursor: pointer;
    border-radius: 5px;
}

.shopltd {
    display: flex;
    justify-content: center;
    margin: 10px 0 3px 0;
}

.router-link-custom {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background-color: var(--default-white);
    border-radius: 0 6px 6px 0;
    text-decoration: none;
}

</style>