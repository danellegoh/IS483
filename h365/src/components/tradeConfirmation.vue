<template>
    <div class="pagePad">
        <selectTrade @card-selected="handleTradeCardSelected" @next="nextStep" />
        <selectYours @card-selected="handleYourCardSelected" @back="previousStep" @next="nextStep" />
        
        <!-- Render the trade confirmation only if both cards are selected -->
        <tradeConfirmation
            v-if="currentStep === 3 && selectedTradeCard && selectedYourCard"
            :trade="{
                card_one_title: selectedTradeCard.title,
                card_one_type: selectedTradeCard.type,
                card_two_title: selectedYourCard.title,
                card_two_type: selectedYourCard.type
            }"
        />
        
        <!-- Card display -->
        <div class="card" v-if="selectedTradeCard && selectedYourCard">
            <div class="cardBottom">
                <div class="offer">
                    <div class="card">
                        <p class="head">Offering Up</p>
                        <img :src="getCardImage(selectedTradeCard.title, selectedTradeCard.type)" />
                        <p class="cardName">{{ selectedTradeCard.title }}</p>
                        <p class="cardSet">{{ selectedTradeCard.type }}</p>
                    </div>
                </div>
                <i class="uil uil-exchange"></i>
                <div class="receive">
                    <div class="card">
                        <p class="head">Requesting For</p>
                        <img :src="getCardImage(selectedYourCard.title, selectedYourCard.type)" />
                        <p class="cardName">{{ selectedYourCard.title }}</p>
                        <p class="cardSet">{{ selectedYourCard.type }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import { defineComponent, ref, watch } from 'vue';
import { defineComponent, ref } from 'vue';
import selectTrade from '../components/selectTrade.vue';
import selectYours from '../components/selectYours.vue';

export default defineComponent({
    components: {
        selectTrade,
        selectYours,
    },
    setup() {
        const currentStep = ref(1);
        const selectedTradeCard = ref(null);
        const selectedYourCard = ref(null);

        const handleTradeCardSelected = (card) => {
            selectedTradeCard.value = card;
            console.log("Selected Trade Card:", selectedTradeCard.value);
        };

        const handleYourCardSelected = (card) => {
            selectedYourCard.value = card;
            console.log("Selected Your Card:", selectedYourCard.value);
        };

        const nextStep = () => {
            if (currentStep.value < 3) {
                currentStep.value++;
            }
        };

        const previousStep = () => {
            if (currentStep.value > 1) {
                currentStep.value--;
            }
        };

        return {
            currentStep,
            selectedTradeCard,
            selectedYourCard,
            handleTradeCardSelected,
            handleYourCardSelected,
            nextStep,
            previousStep,
        };
    }
});
</script>


<!-- <template>
    <div class="pagePad">
        <selectTrade @card-selected="handleTradeCardSelected" @next="nextStep"/>
        <selectYours @card-selected="handleYourCardSelected" @back="previousStep" @next="nextStep"/>
        <tradeConfirmation v-if="currentStep === 3" :trade="{ card_one_title: selectedTradeCard.title, card_one_type: selectedTradeCard.type, card_two_title: selectedYourCard.title, card_two_type: selectedYourCard.type }" />

        <div class="card">
            <div class="cardBottom">
                <div class="offer">
                    <div class="card">
                        <p class="head"> Offering Up </p>
                        <img :src="getCardImage(trade.card_one_title, trade.card_one_type)" />
                        <p class="cardName"> {{ trade.card_one_title }} </p>
                        <p class="cardSet"> {{ trade.card_one_type }} </p>
                    </div>
                </div>
                <i class="uil uil-exchange"></i>
                <div class="receive">
                    <div class="card">
                        <p class="head"> Requesting For </p>
                        <img :src="getCardImage(trade.card_two_title, trade.card_two_type)" />
                        <p class="cardName"> {{ trade.card_two_title }} </p>
                        <p class="cardSet"> {{ trade.card_two_type }} </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent, ref } from 'vue';
import selectTrade from '../components/selectTrade.vue';
import selectYours from '../components/selectYours.vue';
import tradeConfirmation from '../components/tradeConfirmation.vue';

export default defineComponent({
    components: {
        selectTrade,
        selectYours,
        tradeConfirmation,
    },
    setup() {
        const currentStep = ref(1);
        const selectedTradeCard = ref(null);
        const selectedYourCard = ref(null);

        const handleTradeCardSelected = (card) => {
            selectedTradeCard.value = card;
        };

        const handleYourCardSelected = (card) => {
            selectedYourCard.value = card;
        };

        const nextStep = () => {
            if (currentStep.value < 3) {
                currentStep.value++;
            }
        };

        const previousStep = () => {
            if (currentStep.value > 1) {
                currentStep.value--;
            }
        };

        return {
            currentStep,
            selectedTradeCard,
            selectedYourCard,
            handleTradeCardSelected,
            handleYourCardSelected,
            nextStep,
            previousStep,
        };
    }
});
</script>

<style></style> -->