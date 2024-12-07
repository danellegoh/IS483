<template>
    <div class="pagePad">
        <div v-for="(cards, cardType) in availableCards" :key="cardType" class="set">
            <div class="set">
                <p class="cardSet"> {{ cardType }} </p>
                <div class="colDisplay">
                    <div v-for="card in cards" 
                        :key="card.card_id"
                        class="card"
                        :class="{ selected: card.card_id == selectedCard?.card_id }"
                        @click="selectCard(card)"
                        >
                        <p class="cardName"> {{ card.title }} </p>
                        <img :src="getCardImage(card.title, card.collection_id)" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="bookNowContainer">
        <button @click="next" class="nextButton"> Next </button>
    </div>
</template>

<script>
const apiBaseURL = process.env.VUE_APP_API_BASE_URL;

export default {
    data() {
        return {
            allCards: {},
            userCards: [],
            availableCards: {},
            selectedCard: null,
            collectionDataById: {}
        }
    },

    methods: {
        async fetchAllCards() {
            try {
                // const cardReponse = await this.$http.get("http://127.0.0.1:5003/cards");
                const cardReponse = await this.$http.get(`${apiBaseURL}/cards`);
                const cardData = cardReponse.data;

                // const collectionResponse = await this.$http.get("http://127.0.0.1:5022/collections");
                const collectionResponse = await this.$http.get(`${apiBaseURL}/collections`);
                const collectionData = collectionResponse.data.data;
                for (let i = 0; i < collectionData.length; i++) {
                    this.collectionDataById[collectionData[i]["collection_id"]] = {"card_type": collectionData[i]["collection_name"], "expired": collectionData[i]["expired"]}
                }

                const groupedCards = cardData.reduce((acc, card) => {
                    const cardCollectionId = card.collection_id;
                    const cardType = this.collectionDataById[cardCollectionId]["card_type"];
                    if (!acc[cardType]) {
                        acc[cardType] = [];
                    }
                    acc[cardType].push(card);
                    return acc;
                }, {});
                this.allCards = groupedCards;
                this.filterAvailableCards();
            } catch (error) {
                console.error("Error fetching all cards:" + error);
            }
        },

        async fetchUserCards() {
            try {
                // const userResponse = await this.$http.get(`http://127.0.0.1:5006/usercard/user/${this.$store.state.userId}`);
                const userResponse = await this.$http.get(`${apiBaseURL}/usercard/user/${this.$store.state.userId}`);
                this.userCards = userResponse.data.data.cards;
            } catch (error) {
                console.error("Error fetching user cards:", error);
            }
        },

        filterAvailableCards() {
            const ownedCardIds = new Set(this.userCards.map(card => card.card_id));
            const filteredCards = Object.entries(this.allCards).reduce((acc, [cardType, cards]) => {
                const availableCards = cards.filter(card => !ownedCardIds.has(card.card_id));
                if (availableCards.length) {
                    acc[cardType] = availableCards;
                }
                return acc;
            }, {});
            this.availableCards = filteredCards;
            console.log("Filtered available cards:", this.availableCards);
        },

        getCardImage(card_title, card_collection_id) {
            if (!card_title || !card_collection_id) {
                console.error("Invalid card_title or card_collection_id:", card_title, card_collection_id);
                return;
            }

            const formattedTitle = card_title.toLowerCase().replace(/\s+/g, "_");
            const card_set = this.collectionDataById[card_collection_id]["card_type"]
            const formattedSetName = card_set.toLowerCase().replace(/\s+/g, "_");

            console.log(`Fetching image for: ${formattedSetName}/${formattedTitle}.png`);
            try {
                return require(`@/assets/icons/collection/${formattedSetName}/${formattedTitle}.png`);
            } catch (error) {
                console.error(`Image not found for: ${formattedSetName}/${formattedTitle}.png`);
                return;
            }
        },


        selectCard(card) {
            console.log(card);
            this.selectedCard = card;
            this.$emit('card-selected', card);
            // this.$emit('tradeCardSelected', card)
        },

        next() {
            if (this.selectedCard) {
                // this.$emit('card-selected', this.selectedCard);
                this.$emit('next');
            } else {
                alert("Please select a card to proceed.");
            }
        }
    },

    async mounted() {
        await this.fetchUserCards();
        await this.fetchAllCards();
    },
}

</script>

<style scoped>
.pagePad {
    padding: 0 32px;
}

.card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 16px;
    border: none;
}

.card img {
    width: 130px;
}

.card p {
    margin-bottom: 0px;
}

.cardName {
    font-family: text-bold;
    font-size: 17px;
    color: var(--default-text);
    text-align: center;
    line-height: 17px;
}

.cardSet {
    font-family: text-bold;
    font-size: 16px;
    color: var(--text-highlight);
    margin-top: 32px;
    margin-bottom: 0;
}

.cardSet p {
    margin: 0;
}

.colDisplay {
    display: grid;
    grid-template-columns: repeat(2, minmax(130px, 1fr));
    gap: 16px;
    width: 100%;
    padding-top: 16px;
}

.nextButton {
    background-color: var(--blue);
    color: var(--grey);
    font-family: text-medium;
    font-size: 13px;
    border: none;
    width: 100%;
    padding: 25px 0px;
    position: fixed;
    bottom: 0px;
}

.bookNowContainer {
    z-index: 10;
}

.selected {
    border: 3px solid var(--green);
}

</style>