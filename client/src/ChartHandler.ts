import { Chart } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { Data } from "./DataInterface";
import "chartjs-plugin-colorschemes";
import "chartjs-plugin-streaming";
import * as moment from "moment";

Chart.plugins.unregister(ChartDataLabels);

class ChartHandler {
  private dateFormat: string;
  private liveChart: Chart;
  private pieChart: Chart;

  constructor() {
    this.dateFormat = "YYYY-MM-DD H:mm:ss"; // 2019-04-01 16:17:26
  }

  initLiveChart(data: Data) {
    // Config for the chart animation
    const delayInSeconds = 30 * 1000;
    const ttlInSeconds = 90 * 1000;
    const durationInSeconds = 40 * 1000;

    const liveCanvas = <HTMLCanvasElement>document.getElementById("liveChart");
    const liveCtx = liveCanvas.getContext("2d");
    this.liveChart = new Chart(liveCtx, {
      type: "line",
      data: {
        datasets: [{
          label: "Bluetooth",
          data: [],
          fill: false
        }, {
          label: "WiFi",
          data: [],
          fill: false
        }]
      },
      options: {
        title: {
          display: true,
          text: "Estimate of the number of people in the area.",
        },
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: "Time"
            },
            type: "realtime",
            realtime: {
              delay: delayInSeconds,
              duration: durationInSeconds,
              ttl: ttlInSeconds,
            }
          }],
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: "# of People"
            },
            ticks: {
              beginAtZero: true,
              callback: function (value) { if (value % 1 === 0) { return value; } },
              suggestedMax: 10,
              suggestedMin: 0,
            }
          }]
        },
        plugins: {
          colorschemes: {
            scheme: "tableau.ClassicCyclic13"
          }
        },
        tooltips: {
          mode: "nearest",
          intersect: false
        },
        hover: {
          mode: "nearest",
          intersect: false
        },
      }
    });

    let initDate = moment().format(this.dateFormat);
    const animDelayInSeconds = [30, 25, 20];

    // Add "buffer" ticks for a smoother init of the chart
    for (let i = 0; i < data.length; i++) {
      for (let x = 0; x < animDelayInSeconds.length; x++) {
        this.liveChart.data.datasets[i].data.push({
          x: moment(initDate).subtract(animDelayInSeconds[x], "seconds").format(this.dateFormat),
          y: data[i].devices_count
        });
      }
    }

    // Update chart datasets keeping the current animation
    this.liveChart.update({
      preservation: true
    });
  }

  updateLiveChart(data: Data) {
    const btLine = 0;
    const wifiLine = 1;
    let lineToUpdate = btLine;
    const isWifiData = data.sensor_type === "wifi";

    if (isWifiData) {
      lineToUpdate = wifiLine;
    }

    // Append the new data to the existing chart data
    this.liveChart.data.datasets[lineToUpdate].data.push({
      x: data.timestamp,
      y: data.devices_count
    });

    // Update chart datasets keeping the current animation
    this.liveChart.update({
      preservation: true
    });
  }


  // Detection rate of Bluetooth and Wifi
  initPieChart(data: any) {
    const bt_devices_count = data.bt_devices.length;
    const wifi_devices_count = data.wifi_devices.length;

    const pieCanvas = <HTMLCanvasElement>document.getElementById("pieChart");
    const pieCtx = pieCanvas.getContext("2d");
    this.pieChart = new Chart(pieCtx, {
      type: "pie",
      plugins: [ChartDataLabels],
      data: {
        datasets: [{
          label: "Bluetooth",
          data: [bt_devices_count, wifi_devices_count],
          fill: false
        }],
        labels: [
          "Bluetooth",
          "WiFi",
        ]
      },
      options: {
        title: {
          display: true,
          text: "Overall detection rate of Bluetooth vs WiFi."
        },
        plugins: {
          datalabels: {
            color: "#FFF"
          }
        }
      }
    });
  }

  updatePieChart() {
    this.pieChart.data.datasets.forEach((dataset) => {
      dataset.data.push(50, 50, 20, 3);
    });
    this.pieChart.update(
      {
        preservation: true
      }
    );
  }
}

export { ChartHandler };
