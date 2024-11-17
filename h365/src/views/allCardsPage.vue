<template>
    <div class="stickyHeader">
        <div class="pageHeader">
            <i class="uil uil-angle-left" @click="goBack"></i>
            <p> Collection Overview </p>
        </div>
    </div>

    <div class="pagePad" style="margin-top: 32px;">
        <n-breadcrumb>
            <n-breadcrumb-item @click="goTo('collectionPage')">
                My Collection
            </n-breadcrumb-item>

            <n-breadcrumb-item @click="goTo('allCardsPage')">
                Overview
            </n-breadcrumb-item>
        </n-breadcrumb>

        <div class="search-bar">
            <i class="uil uil-search"></i>
            <input type="text" v-model="searchInput" @input="searchCards" placeholder="Search by card or set" />
        </div>

        <div class="head" style="margin-bottom: 5px; padding-top: 25px;">
            <p> Explore Sets </p>
        </div>

        <div v-for="(collection, cardType) in filteredCardsData" :key="cardType" class="set">
            <div class="set">
                <p> {{ cardType }} </p>
                <div class="carousel">
                    <div v-for="card in collection.data" :key="card.card_id" class="card">
                        <p class="cardName"> {{ card.title }} </p>
                        <img :src="getCardImage(card.title, card.collection_id)" />
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    data() {
        return {
            allCards: {},
            collectionDataById: {},
            numCards: 0,
            searchInput: '',
            searchResults: {},
        }
    },

    methods: {
        async fetchAllCards() {
            try {
                const collectionResponse = await this.$http.get("http://127.0.0.1:5022/collections");
                const collections = collectionResponse.data.data;

                this.allCards = {};
                this.collectionDataById = {};

                for (const collection of collections) {
                    const collection_id = collection.collection_id;
                    const collection_name = collection.collection_name;

                    this.collectionDataById[collection_id] = { card_type: collection_name };

                    const cardResponse = await this.$http.get(`http://127.0.0.1:5003/cards/collection/${collection_id}`);
                    const cards = cardResponse.data.data;

                    this.allCards[collection_name] = { data: cards };
                }
                this.numCards = Object.values(this.allCards).reduce((sum, collection) => sum + collection.data.length, 0);
            } catch (error) {
                console.error("Error fetching collections or cards:", error);
            }
        },

        getCardImage(card_title, card_collection_id) {
            const formattedTitle = card_title ? card_title.toLowerCase().replace(/\s+/g, "_") : "default";

            const collectionInfo = this.collectionDataById[card_collection_id];
            const card_set = collectionInfo ? collectionInfo.card_type : "default";
            const formattedSetName = card_set.toLowerCase().replace(/\s+/g, "_");

            try {
                return require(`@/assets/icons/collection/${formattedSetName}/${formattedTitle}.png`);
            } catch (error) {
                console.warn(`Image not found for path.`);
            }
        },

        searchCards() {
            this.searchResults = {};

            if (this.searchInput) {
                const lowerCaseInput = this.searchInput.toLowerCase();

                for (const [type, collection] of Object.entries(this.allCards)) {
                    if (type.toLowerCase().includes(lowerCaseInput)) {
                        this.searchResults[type] = collection;
                    } else {
                        const filteredCards = collection.data.filter(card => card.title.toLowerCase().includes(lowerCaseInput));
                        if (filteredCards.length) {
                            this.searchResults[type] = { data: filteredCards };
                        }
                    }
                }
            } else {
                this.searchResults = {};
            }
        },

        goTo(routeName) {
            this.$router.push({ name: routeName });
        },

        goBack() {
            this.$router.go(-1);
        },
    },

    async mounted() {
        try {
            await this.fetchAllCards();
        } catch (error) {
            console.error("Error during fetchAllCards:", error);
        }
    },

    computed: {
        filteredCardsData() {
            return Object.keys(this.searchResults).length > 0 && this.searchInput
                ? this.searchResults
                : this.allCards;
        },
    },
}
</script>



<style scoped>
.pageHeader {
    background-color: var(--green);
    color: var(--default-white);
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

nav.n-breadcrumb {
    padding-bottom: 16px;
}

.n-breadcrumb {
    font-family: text-regular;
    font-size: 10px;
}

</style>