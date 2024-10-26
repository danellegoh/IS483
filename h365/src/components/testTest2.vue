<template>
    <div class="pagePad">
        <div class="overall-card drop-shadow">
            <div class="offer">
                <div class="card">
                    <p class="head">Offering Up</p>
                    <img :src="getImageSrc(cardGiveSet, cardGiveTitle)">
                    <!-- <img :src="getCardImage(selectedTradeCard.title, selectedTradeCard.type)" /> -->
                    <p class="cardName">{{ cardGiveTitle }}</p>
                    <p class="cardSet">{{ cardGiveSet }}</p>
                </div>
            </div>

            <i class="uil uil-exchange"></i>

            <div class="receive">
                <div class="card">
                    <p class="head">Requesting For</p>
                    <img :src="getImageSrc(cardWantSet, cardWantTitle)">
                    <!-- <img :src="getCardImage(selectedYourCard.title, selectedYourCard.type)" /> -->
                    <p class="cardName">{{ cardWantTitle }}</p>
                    <p class="cardSet">{{ cardWantSet }}</p>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
export default ({
    data() {
        return {
            cardWantTitle: 'Oliver',
            cardWantSet: 'Fruit Basket',
            cardGiveTitle: 'Selena',
            cardGiveSet: 'Fruit Basket',
        }
    },

    methods: {
        getImageSrc(set, title) {
            // console.log("Image source path:", srcPath);
            return require(`@/assets/icons/collection/${set.toLowerCase().replace(/\s+/g, "_")}/${title.toLowerCase()}.png`);
        },
    }
})
</script>

<style>
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
</style>