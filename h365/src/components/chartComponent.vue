<template>
    <div>
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<script>
import { Chart } from 'chart.js/auto';

export default {
    props: {
        chartData: {
            type: Object,
            required: true
        }
    },
    mounted() {
        console.log("Received chartData:", this.chartData);
        this.renderChart();
    },
    methods: {
        renderChart() {
            const ctx = this.$refs.chartCanvas.getContext('2d');
            this.chartInstance = new Chart(ctx, {
                type: 'line',
                data: this.chartData,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                font: {
                                    family: 'text-regular',
                                    size: 12
                                }
                            }
                        },
                        y: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                font: {
                                    family: 'text-regular',
                                    size: 12
                                }
                            }
                        }
                    }
                }
            });
        },
        updateChart() {
            if (this.chartInstance) {
                this.chartInstance.data = this.chartData;
                this.chartInstance.update();
            }
        }
    },
    watch: {
        chartData: {
        deep: true,
        handler() {
            this.updateChart();
        }
        }
    }
}
</script>

<style scoped>
canvas {
    width: 100%;
    height: 400px; /* Adjust height as needed */
}
</style>