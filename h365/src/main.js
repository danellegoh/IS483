import { createApp } from 'vue'
import App from './App.vue'
import router from "./router"
import Chart from 'chart.js/auto';


import { create, NTabs, NTab, NTabPane, NProgress, NSpace } from 'naive-ui'

const naive = create({
    components: [
        NTabs,
        NTab,
        NTabPane,
        NProgress,
        NSpace
    ]
})

// const requireStyles = require.context('@/assets/styling', false, /\\.css$/);
// requireStyles.keys().forEach(fileName => requireStyles(fileName));

createApp(App).use(router).use(naive).mount('#app')