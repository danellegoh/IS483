<template>
    <!-- Info Popup -->
    <div class="card">
        <div class="head">
            <img src="../assets/icons/collection/lightbulb.png">
            <p> Did you know </p>
        </div>

        <p class="cbody">
            {{ cardDescription }}
        </p>

        <div class="head">
            <img src="../assets/icons/collection/recommendation.png">
            <p> Recommendation </p>
        </div>

        <p class="cbody">
        {{ cardRecommendation }}
        </p>

        <div class="coolButton">
            <button style="background-color: var(--blue);" @click="closePopup"> Cool! </button>
        </div>
    </div>

    <div>
        <div class="card">
            <p class="head"> Oops! </p>
            <p class="cbody" style="padding: 0;"> You have already put in a trade in the last 24 hours. </p>
            <div class="coolButton">
                <button style="background-color: var(--blue);" @click="closePopup"> Close </button>
            </div>
        </div>
    </div>

    <!-- <div class="pagePad">
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
    </div> -->
</template>

<script>
// export default ({
//     data() {
//         return {
//             cardWantTitle: 'Oliver',
//             cardWantSet: 'Fruit Basket',
//             cardGiveTitle: 'Selena',
//             cardGiveSet: 'Fruit Basket',
//         }
//     },

//     methods: {
//         getImageSrc(set, title) {
//             return require(`@/assets/icons/collection/${set.toLowerCase().replace(/\s+/g, "_")}/${title.toLowerCase()}.png`);
//         },
//     }
// })


export default {
    props: {
        visible: {
            errorContent: {
                type: String,
                default: 'You have already traded in the last 24 hours!'
            }
        }
    },

    methods: {
        closePopup() {
            this.$emit('close');
        },
    }
}
</script>

<style scoped>

.popupClose {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 32px; /* Increase the size */
    color: white; /* Make it white */
    cursor: pointer;
}

.coolButton {
    display: flex;
    justify-content: center;
}

.card {
    width: 70%;
    display: flex;
    margin: auto;
    padding: 20px;
}

.head {
    font-family: text-bold;
    font-size: 17px;
    color: var(--default-text);
    margin-bottom: 0;
    display: flex;
}

.head img {
    width: 25px;
    height: 25px;
    margin-right: 5px;
}

.container .head p {
    margin-bottom: 5px;
}

.cbody {
    font-family: text-medium;
    font-size: 14px;
    color: var(--default-text);
    padding: 0 8px;
    line-height: 15px;
    text-align: justify;
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


/* .overall-card {
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
} */
</style>