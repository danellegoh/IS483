import { createApp } from 'vue'
import App from './App.vue'
import router from "./router"
import axios from 'axios';
import store from './store';
import './assets/styling/general.css';
import Countdown from 'vue3-flip-countdown'

import { create, NTabs, NTab, NTabPane, NProgress, NSpace, NSteps, NStep, 
    NButtonGroup, NButton, NRadioGroup, NRadioButton, NCheckbox, NDynamicInput, 
    NInputNumber, NInput, NCollapse, NCollapseItem, NBreadcrumb, NBreadcrumbItem } from 'naive-ui'

const naive = create({
    components: [
        NTabs,
        NTab,
        NTabPane,
        NProgress,
        NSpace,
        NSteps,
        NStep,
        NButtonGroup,
        NButton,
        NRadioGroup,
        NRadioButton,
        NCheckbox,
        NDynamicInput,
        NInputNumber,
        NInput,
        NCollapse,
        NCollapseItem,
        NBreadcrumb,
        NBreadcrumbItem,
    ]
})

const app = createApp(App)

app.config.globalProperties.$http = axios;

app.use(router).use(naive).use(store).use(Countdown).mount('#app')