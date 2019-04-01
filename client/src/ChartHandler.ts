import { Data } from "./DataInterface";
import { Chart } from "chart.js";
import "chartjs-plugin-streaming";
import "chartjs-plugin-colorschemes";
import * as moment from "moment";

// Config for the live chart
const delayInSeconds = 30 * 1000;
const ttlInSeconds = 90 * 1000;
const durationInSeconds = 40 * 1000;

const liveCanvas = <HTMLCanvasElement>document.getElementById("liveChart");
const liveCtx = liveCanvas.getContext("2d");
const liveChart = new Chart(liveCtx, {
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


// Config for the pie chart

// Detection rate of Bluetooth and Wifi
const pieCanvas = <HTMLCanvasElement>document.getElementById("pieChart");
const pieCtx = pieCanvas.getContext("2d");
const pieChart = new Chart(pieCtx, {
  type: "pie",
  data: {
    datasets: [{
      label: "Bluetooth",
      data: [2, 10],
      fill: false
    }],
    labels: [
      "Bluetooth",
      "WiFi",
    ]
  },
});


class ChartHandler {
  private dateFormat: string;

  constructor() {
    this.dateFormat = "YYYY-MM-DD H:mm:ss"; // 2019-04-01 16:17:26
  }

  initLiveChart(data: any) {
    let initDate = moment().format(this.dateFormat);
    const delayInSeconds = [30, 25, 20];

    // Add "buffer" ticks for a smoother init of the chart
    for (let i = 0; i < data.length; i++) {
      for (let x = 0; x < delayInSeconds.length; x++) {
        liveChart.data.datasets[i].data.push({
          x: moment(initDate).subtract(delayInSeconds[x], "seconds").format(this.dateFormat),
          y: data[i].devices_count
        });
      }
    }

    // Update chart datasets keeping the current animation
    liveChart.update({
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
    liveChart.data.datasets[lineToUpdate].data.push({
      x: data.timestamp,
      y: data.devices_count
    });

    // Update chart datasets keeping the current animation
    liveChart.update({
      preservation: true
    });
  }

  // updatePeopleCount(data) {
  //   const elem = document.getElementById("peopleCount");
  //   const peopleCount = data[0].devices_count;
  //   const text = `There"s approximately ${peopleCount} person in the area.`
  //   elem.textContent = text;
  // }

}

export { ChartHandler };
