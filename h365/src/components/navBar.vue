<template>
    <nav>
        <ul>
            <div class="navbar">
                <li class="nav-link">
                    <router-link :to="{ name: 'homePage' }" class="nav-item" exact-active-class="active-link">
                        <img
                            class="navIcon"
                            :src="isActiveSection('home') 
                                ? require('../assets/icons/navbar/home_selected.png') 
                                : require('../assets/icons/navbar/home.png')"
                        />
                        <span :class="isActiveSection('home') ? 'active-text' : 'inactive-text'">Home</span>
                    </router-link>
                </li>

                <li class="nav-link">
                    <router-link :to="{ name: 'eventsPage' }" class="nav-item" exact-active-class="active-link">
                        <img
                            class="navIcon"
                            :src="isActiveSection('events') 
                                ? require('../assets/icons/navbar/explore_selected.png') 
                                : require('../assets/icons/navbar/explore.png')"
                        />
                        <span :class="isActiveSection('events') ? 'active-text' : 'inactive-text'">Explore</span>
                    </router-link>
                </li>

                <li class="nav-link">
                    <router-link :to="{ name: 'collectionPage' }" class="nav-item" exact-active-class="active-link">
                        <img
                            class="navIcon"
                            :src="isActiveSection('collection') 
                                ? require('../assets/icons/navbar/collection_selected.png') 
                                : require('../assets/icons/navbar/collection.png')"
                        />
                        <span :class="isActiveSection('collection') ? 'active-text' : 'inactive-text'">Collection</span>
                    </router-link>
                </li>

                <li class="nav-link">
                    <router-link :to="{ name: 'profilePage' }" class="nav-item" exact-active-class="active-link">
                        <img
                            class="navIcon"
                            :src="isActiveSection('profile') 
                                ? require('../assets/icons/navbar/profile_selected.png') 
                                : require('../assets/icons/navbar/profile.png')"
                        />
                        <span :class="isActiveSection('profile') ? 'active-text' : 'inactive-text'">Profile</span>
                    </router-link>
                </li>
            </div>
        </ul>
    </nav>
</template>

<script>
export default {
  methods: {
    // This checks if the current route's meta section matches the given section name
    isActiveSection(section) {
      return this.$route.meta.section === section;
    }
  }
};
</script>

<style scoped>
ul {
    padding-left: 0;
    margin: 0;
}

.navbar {
    display: flex;
    padding: 16px 35px 25px 32px;
    background-color: var(--default-white);
    justify-content: space-between;
    width: 100%;
    position: fixed;
    bottom: 0;
    z-index: 10;
}

.nav-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    justify-content: center;
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.navIcon {
    display: block;
    margin-bottom: 5px;
    width: 20px;
}

.nav-link span {
    font-family: text-semibold;
    font-size: 10.5px;
}

.active-text {
    color: var(--green);
}

.inactive-text {
    color: var(--default-text);
}
</style>