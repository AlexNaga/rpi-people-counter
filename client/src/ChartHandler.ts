import { Chart } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { Data } from "./DataInterface";
import { DataHandler } from "./DataHandler";
import "chartjs-plugin-colorschemes";
import "chartjs-plugin-streaming";
import * as moment from "moment";

Chart.plugins.unregister(ChartDataLabels);
Chart.defaults.global.defaultFontFamily = "'Ubuntu', 'Cantarell'";
Chart.defaults.global.defaultFontSize = 13;

class ChartHandler {
  private dateFormat = "YYYY-MM-DD H:mm:ss"; // 2019-04-01 13:20:45
  private timeFormat = "H:mm:ss"; // 13:20:45
  private liveChart: Chart;
  private pieChart: Chart;
  private dataHandler: DataHandler;

  constructor(dataHandler: DataHandler) {
    this.dataHandler = dataHandler;
  }

  updatePeopleEstimate(data: Data) {
    const btDevicesCount = data[0].devices_count;
    const wifiDevicesCount = data[1].devices_count;
    let pplEstimate = btDevicesCount + wifiDevicesCount;
    const percentOfSmartphoneOwners = 0.9;
    let pplEstimateCorr = Math.round((pplEstimate / percentOfSmartphoneOwners)).toString();

    const pplDiv = document.getElementById("pplValue");
    const pplTopTxtDiv = document.getElementById("pplTopTxt");
    const pplBottomTxtDiv = document.getElementById("pplBottomTxt");
    const pplCorrDiv = document.getElementById("pplCorrValue");
    const pplCorrTopTxtDiv = document.getElementById("pplCorrTopTxt");
    const pplCorrBottomTxtDiv = document.getElementById("pplCorrBottomTxt");
    let pplTopTxt = "";
    let pplBottomTxt = "";
    let pplCorrTopTxt = "";
    let pplCorrBottomTxt = "";

    switch (pplEstimate) {
      case 0:
        pplTopTxt = "Could not detect any devices in the area.";
        pplCorrTopTxt = "Could not detect any devices in the area.";
        pplEstimate = "";
        pplEstimateCorr = "";
        break;
      case 1:
        pplTopTxt = "There is about";
        pplBottomTxt = "person in the area";
        pplCorrTopTxt = pplTopTxt;
        pplCorrBottomTxt = pplBottomTxt;
        break;
      default:
        pplTopTxt = "There are about";
        pplBottomTxt = "people in the area";
        pplCorrTopTxt = pplTopTxt;
        pplCorrBottomTxt = pplBottomTxt;
        break;
    }
    pplDiv.textContent = pplEstimate;
    pplCorrDiv.textContent = pplEstimateCorr;
    pplTopTxtDiv.textContent = pplTopTxt;
    pplBottomTxtDiv.textContent = pplBottomTxt;
    pplCorrTopTxtDiv.textContent = pplCorrTopTxt;
    pplCorrBottomTxtDiv.textContent = pplCorrBottomTxt;
  }


  initLiveChart(data: Data) {
    // Config for the chart animation
    const delayInSeconds = 10 * 1000;
    const ttlInSeconds = 90 * 1000;
    const durationInSeconds = 40 * 1000;

    const liveCanvas = <HTMLCanvasElement>document.getElementById("liveChart");
    const liveCtx = liveCanvas.getContext("2d");
    this.liveChart = new Chart(liveCtx, {
      type: "bar",
      data: {
        datasets: [{
          label: "Bluetooth",
          type: "line",
          data: [],
          fill: false
        }, {
          label: "WiFi",
          type: "line",
          data: [],
          fill: false
        },
        {
          label: "People estimate",
          data: [],
          borderColor: "rgba(197,23,1,0.8)",
          backgroundColor: "rgba(197,23,1,0.4)",
        }]
      },
      options: {
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: "Time",
            },
            barThickness: 30,
            type: "realtime",
            realtime: {
              delay: delayInSeconds,
              duration: durationInSeconds,
              ttl: ttlInSeconds,
            },
            time: {
              unitStepSize: 10,
              displayFormats: {
                hour: "HH",
                minute: "HH:mm",
                second: "HH:mm:ss"
              }
            }
          }],
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: "# Detected"
            },
            ticks: {
              beginAtZero: true,
              callback: (value) => { if (value % 1 === 0) { return value; } },
              suggestedMax: 10,
              suggestedMin: 0,
            }
          }]
        },
        plugins: {
          colorschemes: {
            scheme: "tableau.ClassicCyclic13"
          },
        },
        tooltips: {
          mode: "index",
          intersect: false,
          callbacks: {
            title: (tick) => {
              const date = tick[0].label;
              const timestamp = moment(date, this.dateFormat).format(this.timeFormat);
              return timestamp;
            }
          }
        },
      }
    });

    let initDate = moment().format(this.dateFormat);
    const animDelayInSeconds = [10, 5];

    // Add "buffer" ticks for a smoother init of the chart
    for (let i = 0; i < data.length; i++) {
      for (let x = 0; x < animDelayInSeconds.length; x++) {
        this.liveChart.data.datasets[i].data.push({
          x: moment(initDate, this.dateFormat)
            .subtract(animDelayInSeconds[x], "seconds")
            .format(this.dateFormat),
          y: data[i].devices_count
        });
      }
    }

    const btDevicesCount = data[0].devices_count;
    const wifiDevicesCount = data[1].devices_count;
    const peopleEstimate = btDevicesCount + wifiDevicesCount;

    // "buffer" ticks for the people estimate
    for (let x = 0; x < animDelayInSeconds.length; x++) {
      this.liveChart.data.datasets[2].data.push({
        x: moment(initDate, this.dateFormat)
          .subtract(animDelayInSeconds[x], "seconds")
          .format(this.dateFormat),
        y: peopleEstimate
      });
    }

    // Update chart datasets keeping the current animation
    this.liveChart.update({
      preservation: true
    });
  }

  updateLiveChart(data: Data) {
    const btLine = 0;
    const wifiLine = 1;
    const peopleBar = 2;
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

  updateBarChart(data: Data) {
    const btDevicesCount = data[0].devices_count;
    const wifiDevicesCount = data[1].devices_count;
    const peopleEstimate = btDevicesCount + wifiDevicesCount;
    const peopleBar = 2;

    // Append the new data to the existing chart data
    this.liveChart.data.datasets[peopleBar].data.push({
      x: data[0].timestamp,
      y: peopleEstimate
    });

    // Update chart datasets keeping the current animation
    this.liveChart.update({
      preservation: true
    });
  }


  // Detection rate of Bluetooth and Wifi
  initPieChart(data: any) {
    const btDevicesCount = data.bt_devices_count;
    const wifiDevicesCount = data.wifi_devices_count;
    const totalDevicesCount = btDevicesCount + wifiDevicesCount;

    const pieCanvas = <HTMLCanvasElement>document.getElementById("pieChart");
    const pieCtx = pieCanvas.getContext("2d");
    this.pieChart = new Chart(pieCtx, {
      type: "pie",
      plugins: [ChartDataLabels],
      data: {
        datasets: [{
          data: [btDevicesCount, wifiDevicesCount],
        }],
        labels: [
          "Bluetooth",
          "WiFi",
        ]
      },
      options: {
        legend: {
          reverse: true,
          onClick: (e: any) => e.stopPropagation()
        },
        plugins: {
          datalabels: {
            color: "#000",
            formatter: (value: number, context: object) => {
              const percentage = Math.round((value / totalDevicesCount * 100) * 100) / 100;
              return percentage + "%";
            }
          }
        }
      }
    });
  }

  updatePieChart(data: any) {
    const btDevicesCount = data.bt_devices_count;
    const wifiDevicesCount = data.wifi_devices_count;
    const totalDevicesCount = btDevicesCount + wifiDevicesCount;

    const pieSlices = this.pieChart.data.datasets[0].data;
    const btSlice = 0;
    const wifiSlice = 1;
    pieSlices[btSlice] = btDevicesCount;
    pieSlices[wifiSlice] = wifiDevicesCount;

    // Update the labels
    this.pieChart.options.plugins.datalabels.formatter = (value: number, context: object) => {
      const percentage = Math.round((value / totalDevicesCount * 100) * 100) / 100;
      return percentage + "%";
    }

    this.pieChart.update({ preservation: false });
  }

  private sleep(seconds: number) {
    seconds = seconds * 1000;
    return new Promise(resolve => setTimeout(resolve, seconds));
  }

  async loopPieChartUpdate() {
    this.dataHandler.getStats().then(stats => this.updatePieChart(stats));
    await this.sleep(5);
    this.loopPieChartUpdate() // Recursive call
  }
}

export { ChartHandler };
