<template>
    <div class="pageHeader">
        <p>Tell us more!</p>
    </div>

    <div class="container">
        <div class="banner">
            <div class="text">
                <p class="head"> Tell us more! </p>
                <p class="body"> Help us get to know you better to personalise 
                    your health journey! </p>
            </div>

            <div class="image">
                <img src="../assets/icons/info/icon.png">
            </div>
        </div>
    </div>

    <div class="container">
        <form @submit.prevent="submitProfileDetails">

            <div class="question">
                <div class="label">
                    Height (in CM) 
                    <div class="compulsory">*</div>
                </div>

                <div class="input drop-shadow">
                    <input type="number" v-model="height" name="height" id="height">
                </div>
            </div>

            <div class="question">
                <div class="label">
                    Weight (in KG) 
                    <div class="compulsory">*</div>
                </div>

                <div class="input drop-shadow">
                    <input type="number" v-model="weight" name="weight" id="weight">
                </div>
            </div>

            <div class="question">
                <div class="label">
                    Which school are you from
                    <div class="compulsory">*</div>
                </div>

                <div class="input drop-shadow" @click.stop="toggleSchoolDropdown">
                    <input
                        type="text"
                        v-model="searchSchool"
                        @input="handleSchoolInput"
                        placeholder="Select your school"
                        class="region-input"
                    />

                    <ul v-show="showSchoolDropdown && filteredSchools.length > 0" class="dropdown-list">
                        <li v-for="school in filteredSchools" :key="school.value" @mousedown="selectSchool(school)">
                            {{ school.text }}
                        </li>
                    </ul>
                    <!-- {{ selectedSchool }} -->
                </div>
            </div>

            <div class="question">
                <div class="label">
                    Where do you stay
                    <div class="compulsory">*</div>
                </div>

                <div class="input drop-shadow" @click.stop="toggleRegionDropdown">
                    <input
                        type="text"
                        v-model="searchTerm"
                        @input="handleRegionInput"
                        placeholder="Select your region"
                        class="region-input"
                    />

                    <ul v-show="showDropdown && filteredRegions.length > 0" class="dropdown-list">
                        <li v-for="region in filteredRegions" :key="region.value" @mousedown="selectRegion(region)">
                            {{ region.text }}
                        </li>
                    </ul>
                    <!-- {{ selectedRegion }} -->
                </div>
            </div>

            <button class="formButton" style="color: var(--default-white); 
                background: var(--green); margin-top: 15px;"> <!-- need to add form handling here -->
                Submit
            </button>

        </form>
    </div>
</template>

<style scoped>
.container {
    padding: 32px 32px 0 32px;
}

.banner {
    display: flex;
    background-color: var(--blue);
    border-radius: 6px;
}

.text {
    padding: 16px;
}

.text p {
    margin-bottom: 0;
    color: var(--default-white);
}

.head {
    font-family: text-bold;
    font-size: 18px;
}

.body {
    font-family: text-regular;
    font-size: 14px;
    text-align: justify;
}

.image img {
    width: 120px;
    height: 120px;
}

.question {
    padding-bottom: 16px;
}

.label {
    display: flex;
    margin-bottom: 10px;

    font-family: text-regular;
    font-size: 15px;
    color: var(--text-highlight);
}

.compulsory {
    color: var(--red);
    margin-left: 5px;
}

input {
    border: none;
    width: 100%;
    height: 40px;
    padding: 0 10px;
    font-family: text-medium;
    font-size: 14px;
    color: var(--text-highlight);
}

.input {
    background-color: white;
    border-radius: 6px;
    height: 40px;
}


.school-select {
    width: 100%;
    height: 40px;
    border: none;
    background-color: white;
    border-radius: 6px;
    padding: 0 10px;
    appearance: none;
    display: block;

    font-family: text-medium;
    font-size: 14px;
    color: var(--text-highlight);
}

.region-input, .dropdown-list {
    padding: 0 10px;
    font-family: text-medium;
    font-size: 14px;
    color: var(--text-highlight);
}

.region-input {
    width: 100%;
    height: 40px;
    border: none;
    border-radius: 6px;
    margin-bottom: 8px;
    box-sizing: border-box;
}

.dropdown-list {
    list-style-type: none;
    padding: 10px 10px 0 10px;
    margin: 0;
    position: absolute;
    width: calc(100% - 2px);
    border: 1px solid car(--text-highlight);
    border-radius: 6px;
    background-color: white;
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
    box-sizing: border-box;
}

li {
    padding-bottom: 10px;
}

ul.dropdown-list {
    width: 326px;
}

</style>

<script>
import { useStore } from 'vuex';
import { computed } from 'vue';
import store from '../store';

export default {
    setup() {
        console.log("information page");
        const store = useStore(); // Import useStore from vuex
        const userId = computed(() => store.state.userId); // Access userId from the store
        const userEmail = computed(() => store.state.userEmail) // Access userEmail from the store

        return {
            userId,
            userEmail
        };
    },
    data() {
        return {
            height: null,
            weight: null,

            searchSchool: '',
            selectedSchool: '',
            showSchoolDropdown: false,
            schools: [
                {value:'1', text:'Admiralty Secondary School'},
                {value:'2', text:'Ahmad Ibrahim Secondary School'},
                {value:'3', text:'Anderson Secondary School'},
                {value:'4', text:'Anglican High School'},
                {value:'5', text:'Anglo-Chinese School (Barker Road)'},
                {value:'6', text:'Anglo-Chinese School (Independent)'},
                {value:'7', text:'Ang Mo Kio Secondary School'},
                {value:'8', text:'Assumption English School'},
                {value:'9', text:'Bartley Secondary School'},
                {value:'10', text:'Beatty Secondary School'},
                {value:'11', text:'Bedok Green Secondary School'},
                {value:'12', text:'Bedok South Secondary School'},
                {value:'13', text:'Bedok View Secondary School'},
                {value:'14', text:'Bendemeer Secondary School'},
                {value:'15', text:'Boon Lay Secondary School'},
                {value:'16', text:'Bowen Secondary School'},
                {value:'17', text:'Broadrick Secondary School'},
                {value:'18', text:'Bukit Batok Secondary School'},
                {value:'19', text:'Bukit Merah Secondary School'},
                {value:'20', text:'Bukit Panjang Government High School'},
                {value:'21', text:'Bukit View Secondary School'},
                {value:'22', text:'Catholic High School'},
                {value:'23', text:'Canberra Secondary School'},
                {value:'24', text:'Cedar Girls\' Secondary School'},
                {value:'25', text:'Changkat Changi Secondary School'},
                {value:'26', text:'CHIJ Katong Convent (Secondary)'},
                {value:'27', text:'CHIJ Secondary (Toa Payoh)'},
                {value:'28', text:'CHIJ St. Joseph\'s Convent'},
                {value:'29', text:'CHIJ St. Nicholas Girls\' School'},
                {value:'30', text:'CHIJ St. Theresa\'s Convent'},
                {value:'31', text:'Chua Chu Kang Secondary School'},
                {value:'32', text:'Christ Church Secondary School'},
                {value:'33', text:'Chung Cheng High School (Main)'},
                {value:'34', text:'Chung Cheng High School (Yishun)'},
                {value:'35', text:'Clementi Town Secondary School'},
                {value:'36', text:'Commonwealth Secondary School'},
                {value:'37', text:'Compassvale Secondary School'},
                {value:'38', text:'Crescent Girls\' School'},
                {value:'39', text:'Damai Secondary School'},
                {value:'40', text:'Deyi Secondary School'},
                {value:'41', text:'Dunearn Secondary School'},
                {value:'42', text:'Dunman High School'},
                {value:'43', text:'Dunman Secondary School'},
                {value:'44', text:'East Spring Secondary School'},
                {value:'45', text:'Edgefield Secondary School'},
                {value:'46', text:'Evergreen Secondary School'},
                {value:'47', text:'Fairfield Methodist Secondary School'},
                {value:'48', text:'Fuchun Secondary School'},
                {value:'49', text:'Fuhua Secondary School'},
                {value:'50', text:'Gan Eng Seng School'},
                {value:'51', text:'Geylang Methodist School (Secondary)'},
                {value:'52', text:'Greendale Secondary School'},
                {value:'53', text:'Greenridge Secondary School'},
                {value:'54', text:'Guangyang Secondary School'},
                {value:'55', text:'Hai Sing Catholic School'},
                {value:'56', text:'Hillgrove Secondary School'},
                {value:'57', text:'Holy Innocents\' High School'},
                {value:'58', text:'Hougang Secondary School'},
                {value:'59', text:'Hua Yi Secondary School'},
                {value:'60', text:'Hwa Chong Institution'},
                {value:'61', text:'Junyuan Secondary School'},
                {value:'62', text:'Jurong Secondary School'},
                {value:'63', text:'Jurong West Secondary School'},
                {value:'64', text:'Jurongville Secondary School'},
                {value:'65', text:'Juying Secondary School'},
                {value:'66', text:'Kent Ridge Secondary School'},
                {value:'67', text:'Kranji Secondary School'},
                {value:'68', text:'Kuo Chuan Presbyterian Secondary School'},
                {value:'69', text:'Loyang View Secondary School'},
                {value:'70', text:'Manjusri Secondary School'},
                {value:'71', text:'Maris Stella High School'},
                {value:'72', text:'Marsiling Secondary School'},
                {value:'73', text:'Mayflower Secondary School'},
                {value:'74', text:'Meridian Secondary School'},
                {value:'75', text:'Methodist Girls\' School (Secondary)'},
                {value:'76', text:'Montfort Secondary School'},
                {value:'77', text:'Nan Chiau High School'},
                {value:'78', text:'Nan Hua High School'},
                {value:'79', text:'Nanyang Girls\' High School'},
                {value:'80', text:'National Junior College'},
                {value:'81', text:'Naval Base Secondary School'},
                {value:'82', text:'New Town Secondary School'},
                {value:'83', text:'Ngee Ann Secondary School'},
                {value:'84', text:'North Vista Secondary School'},
                {value:'85', text:'Northbrooks Secondary School'},
                {value:'86', text:'Northland Secondary School'},
                {value:'87', text:'NUS High School of Mathematics and Science'},
                {value:'88', text:'Orchid Park Secondary School'},
                {value:'89', text:'Outram Secondary School'},
                {value:'90', text:'Pasir Ris Crest Secondary School'},
                {value:'91', text:'Pasir Ris Secondary School'},
                {value:'92', text:'Paya Lebar Methodist Girls\' School (Secondary)'},
                {value:'93', text:'Pei Hwa Secondary School'},
                {value:'94', text:'Peicai Secondary School'},
                {value:'95', text:'Peirce Secondary School'},
                {value:'96', text:'Presbyterian High School'},
                {value:'97', text:'Punggol Secondary School'},
                {value:'98', text:'Queenstown Secondary School'},
                {value:'99', text:'Queensway Secondary School'},
                {value:'100', text:'Raffles Girls\' School (Secondary)'},
                {value:'101', text:'Raffles Institution'},
                {value:'102', text:'Regent Secondary School'},
                {value:'103', text:'Riverside Secondary School'},
                {value:'104', text:'River Valley High School'},
                {value:'105', text:'St. Andrew\'s Secondary School'},
                {value:'106', text:'St. Patrick\'s School'},
                {value:'107', text:'School of Science and Technology, Singapore'},
                {value:'108', text:'School of the Arts, Singapore'},
                {value:'109', text:'Sembawang Secondary School'},
                {value:'110', text:'Sengkang Secondary School'},
                {value:'111', text:'Serangoon Garden Secondary School'},
                {value:'112', text:'Serangoon Secondary School'},
                {value:'113', text:'Singapore Chinese Girls\' School'},
                {value:'114', text:'Singapore Sports School'},
                {value:'115', text:'Springfield Secondary School'},
                {value:'116', text:'St. Anthony\'s Canossian Secondary School'},
                {value:'117', text:'St. Gabriel\'s Secondary School'},
                {value:'118', text:'St. Hilda\'s Secondary School'},
                {value:'119', text:'St. Margaret\'s Secondary School'},
                {value:'120', text:'St. Joseph\'s Institution'},
                {value:'121', text:'Swiss Cottage Secondary School'},
                {value:'122', text:'Tanglin Secondary School'},
                {value:'123', text:'Tampines Secondary School'},
                {value:'124', text:'Tanjong Katong Girls\' School'},
                {value:'125', text:'Tanjong Katong Secondary School'},
                {value:'126', text:'Temasek Junior College'},
                {value:'127', text:'Temasek Secondary School'},
                {value:'128', text:'Unity Secondary School'},
                {value:'129', text:'Victoria School'},
                {value:'130', text:'West Spring Secondary School'},
                {value:'131', text:'Westwood Secondary School'},
                {value:'132', text:'Whitley Secondary School'},
                {value:'133', text:'Woodgrove Secondary School'},
                {value:'134', text:'Woodlands Ring Secondary School'},
                {value:'135', text:'Woodlands Secondary School'},
                {value:'136', text:'Xinmin Secondary School'},
                {value:'137', text:'Yio Chu Kang Secondary School'},
                {value:'138', text:'Yishun Secondary School'},
                {value:'139', text:'Yishun Town Secondary School'},
                {value:'140', text:'Yuan Ching Secondary School'},
                {value:'141', text:'Yuhua Secondary School'},
                {value:'142', text:'Yusof Ishak Secondary School'},
                {value:'143', text:'Yuying Secondary School'},
                {value:'144', text:'Zhenghua Secondary School'},
                {value:'145', text:'Zhonghua Secondary School'},
                {value:'146', text:'Anderson Serangoon Junior College'},
                {value:'147', text:'Anglo-Chinese Junior College'},
                {value:'148', text:'Anglo-Chinese IB Junior College'},
                {value:'149', text:'Catholic Junior College'},
                {value:'150', text:'Eunoia Junior College'},
                {value:'151', text:'Jurong Pioneer Junior College'},
                {value:'152', text:'Nanyang Junior College'},
                {value:'153', text:'Saint Andrew\'s Junior College'},
                {value:'154', text:'Tampines Meridian Junior College'},
                {value:'155', text:'Victoria Junior College'},
                {value:'156', text:'Yishun Innova Junior College'},
                {value:'157', text:'Singapore Polytechnic'},
                {value:'158', text:'Ngee Ann Polytechnic'},
                {value:'159', text:'Temasek Polytechnic'},
                {value:'160', text:'Nanyang Polytechnic'},
                {value:'161', text:'Republic Polytechnic'},
                {value:'162', text:'ITE College Central'},
                {value:'163', text:'ITE College West'},
                {value:'164', text:'ITE College East'},
            ],
            filteredSchools: [],

            searchTerm: '',
            selectedRegion: '',
            showDropdown: false,
            regions: [
                {value:  "admiralty", text:  "Admiralty"},
                {value:  "ang mo kio", text:  "Ang Mo Kio"},
                {value:  "bayfront", text:  "Bayfront"},
                {value:  "bedok reservoir", text:  "Bedok Reservoir"},
                {value:  "bencoolen", text:  "Bencoolen"},
                {value:  "bendemeer", text:  "Bendemeer"},
                {value:  "boon lay", text:  "Boon Lay"},
                {value:  "braddell", text:  "Braddell"},
                {value:  "bras basah", text:  "Bras Basah"},
                {value:  "bright hill", text:  "Bright Hill"},
                {value:  "bukit batok", text:  "Bukit Batok"},
                {value:  "bukit ho swee", text:  "Bukit Ho Swee"},
                {value:  "bukit merah", text:  "Bukit Merah"},
                {value:  "bukit panjang", text:  "Bukit Panjang"},
                {value:  "buona vista", text:  "Buona Vista"},
                {value:  "caldecott", text:  "Caldecott"},
                {value:  "canberra", text:  "Canberra"},
                {value:  "changi airport", text:  "Changi Airport"},
                {value:  "changi", text:  "Changi"},
                {value:  "chinatown", text:  "Chinatown"},
                {value:  "choa chu kang", text:  "Choa Chu Kang"},
                {value:  "city hall", text:  "City Hall"},
                {value:  "clarke quay", text:  "Clarke Quay"},
                {value:  "clementi west", text:  "Clementi West"},
                {value:  "clementi", text:  "Clementi"},
                {value:  "commonwealth", text:  "Commonwealth"},
                {value:  "dhoby ghaut", text:  "Dhoby Ghaut"},
                {value:  "dover", text:  "Dover"},
                {value:  "downtown", text:  "Downtown"},
                {value:  "esplanade", text:  "Esplanade"},
                {value:  "eunos", text:  "Eunos"},
                {value:  "expo", text:  "Expo"},
                {value:  "farrer park", text:  "Farrer Park"},
                {value:  "farrer road", text:  "Farrer Road"},
                {value:  "gardens by the bay", text:  "Gardens By The Bay"},
                {value:  "geylang bahru", text:  "Geylang Bahru"},
                {value:  "golden mile", text:  "Golden Mile"},
                {value:  "goldhill plaza", text:  "Goldhill Plaza"},
                {value:  "gul circle", text:  "Gul Circle"},
                {value:  "harbourfront", text:  "Harbourfront"},
                {value:  "havelock road", text:  "Havelock Road"},
                {value:  "havelock", text:  "Havelock"},
                {value:  "holland village", text:  "Holland Village"},
                {value:  "jalan besar", text:  "Jalan Besar"},
                {value:  "joo koon", text:  "Joo Koon"},
                {value:  "jurong east", text:  "Jurong East"},
                {value:  "jurong pier", text:  "Jurong Pier"},
                {value:  "kaki bukit", text:  "Kaki Bukit"},
                {value:  "kallang", text:  "Kallang"},
                {value:  "kembangan", text:  "Kembangan"},
                {value:  "kent ridge", text:  "Kent Ridge"},
                {value:  "keong saik", text:  "Keong Saik"},
                {value:  "lakeside", text:  "Lakeside"},
                {value:  "little india", text:  "Little India"},
                {value:  "loyang", text:  "Loyang"},
                {value:  "macpherson", text:  "Macpherson"},
                {value:  "marina barrage", text:  "Marina Barrage"},
                {value:  "marina bay sands", text:  "Marina Bay Sands"},
                {value:  "marina bay", text:  "Marina Bay"},
                {value:  "marina south pier", text:  "Marina South Pier"},
                {value:  "marsiling", text:  "Marsiling"},
                {value:  "maxwell", text:  "Maxwell"},
                {value:  "mayflower", text:  "Mayflower"},
                {value:  "mountbatten", text:  "Mountbatten"},
                {value:  "napier", text:  "Napier"},
                {value:  "newton", text:  "Newton"},
                {value:  "novena", text:  "Novena"},
                {value:  "one north", text:  "One North"},
                {value:  "orchard boulevard", text:  "Orchard Boulevard"},
                {value:  "outram park", text:  "Outram Park"},
                {value:  "pasir ris", text:  "Pasir Ris"},
                {value:  "paya lebar", text:  "Paya Lebar"},
                {value:  "paya lebar", text:  "Paya Lebar"},
                {value:  "pioneer", text:  "Pioneer"},
                {value:  "promenade", text:  "Promenade"},
                {value:  "queenstown", text:  "Queenstown"},
                {value:  "raffles place", text:  "Raffles Place"},
                {value:  "raffles quay", text:  "Raffles Quay"},
                {value:  "rochor", text:  "Rochor"},
                {value:  "sembawang", text:  "Sembawang"},
                {value:  "simei", text:  "Simei"},
                {value:  "somerset", text:  "Somerset"},
                {value:  "springleaf", text:  "Springleaf"},
                {value:  "stamford", text:  "Stamford"},
                {value:  "tagore", text:  "Tagore"},
                {value:  "tai seng", text:  "Tai Seng"},
                {value:  "tampines east", text:  "Tampines East"},
                {value:  "tampines west", text:  "Tampines West"},
                {value:  "tampines", text:  "Tampines"},
                {value:  "tan kah kee", text:  "Tan Kah Kee"},
                {value:  "tanah merah", text:  "Tanah Merah"},
                {value:  "tanjong pagar", text:  "Tanjong Pagar"},
                {value:  "telok ayer", text:  "Telok Ayer"},
                {value:  "telok blangah", text:  "Telok Blangah"},
                {value:  "tiong bahru", text:  "Tiong Bahru"},
                {value:  "toa payoh", text:  "Toa Payoh"},
                {value:  "tuas", text:  "Tuas"},
                {value:  "ubi", text:  "Ubi"},
                {value:  "ubis", text:  "Ubis"},
                {value:  "upper thomson", text:  "Upper Thomson"},
                {value:  "woodlands north", text:  "Woodlands North"},
                {value:  "woodlands south", text:  "Woodlands South"},
                {value:  "yio chu kang", text:  "Yio Chu Kang"},
                {value:  "yishun", text:  "Yishun"},
                {value: "aljunied", text: "Aljunied"},
                {value: "bedok north", text: "Bedok North"},
                {value: "bedok", text: "Bedok"},
                {value: "botanic gardens", text: "Botanic Gardens"},
                {value: "bugis", text: "Bugis"},
                {value: "bukit timah", text: "Bukit Timah"},
                {value: "dakota", text: "Dakota"},
                {value: "fort canning", text: "Fort Canning"},
                {value: "great world", text: "Great World"},
                {value: "haw par villa", text: "Haw Par Villa"},
                {value: "jalan bahar", text: "Jalan Bahar"},
                {value: "jurong west", text: "Jurong West"},
                {value: "keppel", text: "Keppel"},
                {value: "khatib", text: "Khatib"},
                {value: "lentor", text: "Lentor"},
                {value: "orchard", text: "Orchard"},
                {value: "redhill", text: "Redhill"},
                {value: "sentosa", text: "Sentosa"},
                {value: "stevens", text: "Stevens"},
                {value: "tengah", text: "Tengah"},
                {value: "upper changi", text: "Upper Changi"},
                {value: "woodlands", text: "Woodlands"},
            ],
            filteredRegions: []
        }
    },
    methods: {
        toggleSchoolDropdown() {
            this.showSchoolDropdown = !this.showSchoolDropdown;
            this.showDropdown  = false;
        },

        toggleRegionDropdown() {
            this.showDropdown = !this.showDropdown;
            this.showSchoolDropdown  = false;
        },

        closeDropdowns() {
            this.showSchoolDropdown  = false;
            this.showDropdown  = false;
        },

        filterRegions() {
            this.filteredRegions = this.regions.filter(region =>
            region.text.toLowerCase().includes(this.searchTerm.toLowerCase())
            );
        },
        selectRegion(region) {
            this.searchTerm = region.text;
            this.selectedRegion = region.value;
            this.showDropdown = false;
        },

        filterSchools() {
            this.filteredSchools = this.schools.filter(school =>
            school.text.toLowerCase().includes(this.searchSchool.toLowerCase())
            );
        },
        selectSchool(school) {
            this.searchSchool = school.text;
            this.selectedSchool = school.value;
            this.showSchoolDropdown = false;
        },

        clearSelectedSchool() {
            if (this.selectedSchool) {
                this.selectedSchool = null;
                this.searchSchool = '';
            }
        },

        clearSelectedRegion() {
            if (this.selectedRegion) {
                this.selectedRegion = null;
                this.searchTerm = '';
            }
        },

        handleRegionInput() {
            this.clearSelectedRegion();
            this.filterRegions();
        },

        handleSchoolInput() {
            this.clearSelectedSchool();
            this.filterSchools();
        },

        async submitProfileDetails() {
            console.log("Submission attempt");
            console.log("Height:", this.height);
            console.log("Weight:", this.weight);
            console.log("Selected School:", this.searchSchool);
            console.log("Selected Region:", this.searchTerm);

            try {
                console.log("Update information attempt");
                console.log("Current Store State:", store.state);
                console.log(this.userEmail);
                const response = await this.$http.patch("http://127.0.0.1:5001/user/" + this.userEmail, {
                        height: this.height,
                        weight: this.weight,
                        school: this.searchSchool,
                        location_group: this.searchTerm
                })
                console.log(response);

                this.$router.push('/goal');
            }
            catch (error) {
                console.log(error);
            }
        }
    },

    mounted() {
        this.filteredRegions = this.regions;
        this.filteredSchools = this.schools;
        document.addEventListener("click", this.closeDropdowns);
    },

    beforeUnmount() {
        document.removeEventListener("click", this.closeDropdowns);
    }
}
</script>