<template>
    <div>
        <div class="stickyHeader">
            <div class="pageHeader">
                <i class="uil uil-angle-left" @click="goBack"></i>
                <p> Your Monthly Report </p>
            </div>
        </div>

        <div class="pagePad" id="results">
            <div class="reportHeader">
                <p class="actual">{{ lastMonth }} Report</p>
            </div>

            <div class="colDisplay">
                <div>
                    <div class="card drop-shadow">
                        <div class="content">
                                <p class="actual"> {{ mr_topActivity }} </p>
                                <p class="label"> Top Activity </p>
                                <img src="../assets/icons/report/trophy.png" class="cardimg">
                        </div>

                    </div>
                </div>

                <div>
                    <div class="card drop-shadow">
                        <div class="content">
                                <p class="actual"> {{ streakCount }} </p>
                                <p class="label"> Current Streak </p>
                                <img src="../assets/icons/report/streak.png" class="cardimg">
                        </div>

                    </div>
                </div>
            </div>


            <div class="colDisplay">
                <div>
                    <div class="card drop-shadow">
                        <div class="content">
                                <p class="actual"> {{ mr_totalDistance }} KM </p>
                                <p class="label"> Total Distance </p>
                                <img src="../assets/icons/report/distance.png" class="cardimg">
                                <!-- <p class="sublabel"> +13% </p> -->
                        </div>

                    </div>
                </div>

                <div>
                    <div class="card drop-shadow">
                        <div class="content">
                                <p class="actual"> {{ mr_movingMinutes }} </p>
                                <p class="label"> Moving Minutes </p>
                                <img src="../assets/icons/report/time.png" class="cardimg">
                                <!-- <p class="sublabel"> +10% </p> -->
                        </div>

                    </div>
                </div>
            </div>


            <div class="card drop-shadow chartContainer">
                <div class="content">
                    <p class="actual" style="font-size: 15px; margin-bottom: 5px;"> Activity Recorded </p>
                    <div class="chart">
                        <ChartComponent :chartData="chartData" style="height: 200px; width: 100%;"/>
                    </div>
                </div>
            </div>

        </div>  
        
        <div class="bookNowContainer">
            <button class="bookButton" @click="generatePDF"> 
            Save Report </button>
        </div>
    </div>

</template>

<script>
import ChartComponent from '@/components/chartComponent.vue';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
// import { markRaw } from 'vue';

export default {
  components: {
    ChartComponent
  },

  data() {
    return {
        chartData: {
            labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
            // labels: [],
            datasets: [
                {
                    data: [],
                    // data: [0, 0, 0, 0, 0, 0, 6001.5, 0, 0, 0, 0, 0, 0, 5708.5, 0, 0, 0, 0, 0, 0, 7104.9, 0, 0, 0, 0, 0, 0, 6006.2, 0, 0],
                    fill: false,
                    borderColor: 'rgb(28, 131, 225)',
                    tension: 0.1,
                    pointBackgroundColor: 'white',
                    pointRadius: 3
                }
            ]
        },
        streakCount: this.$route.params.streakCount || 0,
        mr_movingMinutes: this.$route.params.mr_movingMinutes || 154,
        mr_topActivity: this.$route.params.mr_topActivity || "Run",
        mr_totalDistance: Math.round((this.$route.params.mr_totalDistance / 1000), 2) || 31,
        mr_allActivitites: {},
        mr_month: this.$route.params.mr_month || 0,
        lastMonth: "",
        temp: []
    };
  },

  mounted() {
    console.log('Route params:', this.$route.params);

    if (this.$route.params.mr_allActivitites) {
        try {
            this.mr_allActivitites = JSON.parse(this.$route.params.mr_allActivitites);
            console.log('Parsed Activities:', this.mr_allActivitites);
            this.populateChartData();
        } catch (error) {
            console.error("Error parsing mr_allActivitites:", error);
        }
    } else {
        console.error("mr_allActivitites is undefined.");
    }

    this.getPreviousMonth();
  },

  methods: {
    populateChartData() {
        const totalDaysInMonth = new Date(2024, this.mr_month, 0).getDate();

        // // Create a shallow copy of chartData to avoid triggering unnecessary reactivity loops
        // const newChartData = { ...this.chartData };

        // // Update labels with a shallow copy
        // newChartData.labels = Array.from({ length: totalDaysInMonth }, (_, i) => i + 1);
        // console.log(newChartData.labels);

        // const activities = this.mr_allActivitites;
        // this.temp = [];

        // // Populate temp array with activity data
        // for (let i = 1; i <= totalDaysInMonth; i++) {
        //     if (activities[i]) {
        //         this.temp.push(activities[i]);
        //     } else {
        //         this.temp.push(0);
        //     }
        // }

        // console.log("haha", this.temp);

        // // Update datasets[0].data with a shallow copy
        // newChartData.datasets = [...this.chartData.datasets];
        // newChartData.datasets[0] = { ...this.chartData.datasets[0], data: [...this.temp] };

        // // Replace the entire chartData object with the updated copy
        // // this.chartData = newChartData;

        // this.chartData = markRaw(newChartData);

        // console.log("Populated Chart Data:", this.chartData.datasets[0].data);
        // Generate labels for each day in the month
        const labels = Array.from({ length: totalDaysInMonth }, (_, i) => i + 1);

        // Populate data for each day from `mr_allActivitites`
        const data = labels.map(day => this.mr_allActivitites[day] || 0);

        // Update chartData by creating a new object to trigger reactivity
        this.chartData = {
        labels,
        datasets: [
            {
            data,
            fill: false,
            borderColor: 'rgb(28, 131, 225)',
            tension: 0.1,
            pointBackgroundColor: 'white',
            pointRadius: 3
            }
        ]
        };

        console.log("Updated Chart Data:", this.chartData.datasets[0].data);
        console.log("chartData before passing to ChartComponent:", this.chartData);

    },
    goBack() {
        this.$router.go(-1);
    },
    getPreviousMonth() {
        const currentDate = new Date();
        let month = currentDate.getMonth();

        if (month === 0) {
            month = 11;
        } else {
            month -= 1;
        }

        // Get the month name from the month index
        const monthNames = ["January", "February", "March", "April", "May", "June", 
                            "July", "August", "September", "October", "November", "December"];
        this.lastMonth = monthNames[month];
    },
    generatePDF() {
        const toPrint = document.getElementById('results');
        
        // Hide sticky header during export
        const stickyHeader = document.querySelector('.stickyHeader');
        stickyHeader.style.display = 'none'; 

        // Ensure that the entire area to be captured is visible
        window.scrollTo(0, 0);

        html2canvas(toPrint, {
            scale: 2, // Adjust scale for better resolution if needed
            backgroundColor: '#F5F4F1',
            useCORS: true, // If you're using external resources like images
            x: toPrint.offsetLeft,
            y: toPrint.offsetTop,
            width: toPrint.scrollWidth, // Ensure entire width is captured
            height: toPrint.scrollHeight, // Ensure entire height is captured
            scrollX: 0,
            scrollY: 0,
        }).then((canvas) => {
            // Get the canvas and convert it to an image data URL
            const imgData = canvas.toDataURL('image/png');

            // Calculate the correct width and height for the PDF
            const pdfWidth = 210; // A4 width in mm
            const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

            const pdf = new jsPDF({
                orientation: 'portrait',
                unit: 'mm',
                format: [pdfWidth, pdfHeight],
                margins: { top: 10, left: 10, right: 10, bottom: 10 }
            });

            // Add image to the PDF
            pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);

            // Save the PDF
            pdf.save('Monthly_Report.pdf');

            // Restore the sticky header after the export
            stickyHeader.style.display = 'block'; 
        });
    }
    }
};
</script>

<style scoped>
.pagePad {
    padding: 20px 32px 32px 32px;
}

.pageHeader {
    background-color: var(--orange);
    color: var(--default-white);
}

.card {
    border: none;
}

.content {
    padding: 20px;
}

.heading {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
}

.heading img {
    width: 45px;
    height: 45px;
}

.heading p {
    font-family: text-semibold;
    font-size: 14px;
    color: var(--default-text);
    margin-bottom: 0;
}

.colDisplay {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    width: 100%;
    padding-bottom: 16px;
}

.actual, .label {
    margin-bottom: 0;
    text-align: center;
}

.actual {
    font-family: text-bold;
    font-size: 20px;
    color: var(--text-highlight);
}

.label {
    font-family: text-medium;
    font-size: 14px;
    color: var(--text-highlight);
    margin-bottom: 5px;
}

/* .sublabel {
    display: inline-block;
    font-family: text-regular;
    font-size: 10px;
    margin: 5px 0;
    text-align: center;
    background-color: var(--green);
    color: var(--default-white);
    border-radius: 6px;
    padding: 3px 8px;
    align-items: center;
} */

.cardimg {
    width: 50px;
    height: auto;
    display: flex;
    margin: auto;
}

.reportHeader {
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
}

.chartContainer {
    margin-bottom: 16px;
}

.buttonContainer {
    display: flex;
    justify-content: center;
    align-items: center;
}

.bookButton {
    background-color: var(--blue);
    color: var(--grey);
    font-family: text-medium;
    font-size: 13px;
    border: none;
    width: 100%;
    padding: 16px 0px;
    position: fixed;
    bottom: 81.75px;
}

.bookNowContainer {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
    z-index: 10;
}

</style>