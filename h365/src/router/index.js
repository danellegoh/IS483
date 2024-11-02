import { createRouter, createWebHistory } from "vue-router";

const routes = [
    {
        path: "/",
        name: "loginPage",
        component: () => import("@/views/loginPage.vue"),
        meta: { hideNavBar: true }
    },

    {
        path: "/info",
        name: "informationPage",
        component: () => import("@/views/informationPage.vue"),
        meta: { hideNavBar: true }
    },

    {
        path: "/goal",
        name: "goalSettingPage",
        component: () => import("@/views/goalSettingPage.vue"),
        meta: { hideNavBar: true }
    },

    {
      path: "/home",
      name: "homePage",
      component: () => import("@/views/homePage.vue"),
      meta: { section: 'home' }
    },

    {
      path: "/report",
      name: "monthlyReport",
      component: () => import("@/views/monthlyReport.vue"),
      props: true,
      meta: { section: 'home' }
    },

    {
      path: "/events",
      name: "eventsPage",
      component: () => import("@/views/eventsPage.vue"),
      meta: { section: 'events' }
    },

    {
      path: "/booked",
      name: "bookedEventsPage",
      component: () => import("@/views/bookedEventsPage.vue"),
      meta: { section: 'events' }
    },

    {
      path: "/event/:eventId",
      name: "viewEventPage",
      component: () => import("@/views/viewEventPage.vue"),
      meta: { section: 'events' }
    },

    {
      path: "/collection",
      name: "collectionPage",
      component: () => import("@/views/collectionPage.vue"),
      meta: { section: 'collection' }
    },

    // {
    //   path: "/popup",
    //   name: "popup",
    //   component: () => import("@/components/popUp.vue"),
    // },

    {
      path: "/store",
      name: "storePage",
      component: () => import("@/views/storePage.vue"),
      meta: { section: 'collection' }
    },

    {
      path: "/trade",
      name: "tradePage",
      component: () => import("@/views/tradePage.vue"),
      meta: { section: 'collection' }
    },

    {
      path: "/mytrades",
      name: "myTradesPage",
      component: () => import("@/views/myTradesPage.vue"),
      meta: { section: 'collection' }
    },

    {
      path: "/newTrade",
      name: "newTradePage",
      component: () => import("@/views/newTradePage.vue"),
      meta: { hideNavBar: true }
    },

    // {
    //   path: "/test",
    //   name: "testTest",
    //   component: () => import("@/components/testTest2.vue"),
    //   meta: { hideNavBar: true }
    // },

    {
      path: "/profile",
      name: "profilePage",
      component: () => import("@/views/profilePage.vue"),
      meta: { section: 'profile' }
    },

    {
      path: "/admin",
      name: "adminPage",
      component: () => import("@/views/adminPage.vue"),
      meta: { 
        requiresAdmin: true,
        hideNavBar: true 
      }
    }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  // mode: "history",
  routes,
});

router.beforeEach((to, from, next) => {
  const userRole = sessionStorage.getItem('userRole');

  if (to.meta.requiresAdmin && userRole != 'Admin') {
    next({ name: 'loginPage' });
  } else {
    next();
  }
  
})
  
export default router;