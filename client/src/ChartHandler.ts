import { Data } from "./DataInterface";

// Config
const delayInSeconds = 30 * 1000;
const ttlInSeconds = 90 * 1000;
const durationInSeconds = 40 * 1000;

const canvas = <HTMLCanvasElement>document.getElementById("liveChart");
const ctx = canvas.getContext("2d");

const liveChart = new Chart(ctx, {
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
  }
});

class ChartHandler {
  constructor() {
  }

  initLiveChart(data: any) {
    const initDate = new Date();
    const delayTime = [[30, 5], [5, 5]];

    for (let i = 0; i < data.length; i++) {
      liveChart.data.datasets[i].data.push({
        x: initDate.setSeconds(initDate.getSeconds() - delayTime[i][0]),
        y: data[i].devices_count
      });

      liveChart.data.datasets[i].data.push({
        x: initDate.setSeconds(initDate.getSeconds() + delayTime[i][1]),
        y: data[i].devices_count
      });
    }

    // Update chart datasets keeping the current animation
    liveChart.update({
      preservation: true
    });
  }

  // createLiveChart(data) {
  //   const dataList = [];

  //   data.forEach(i => {
  //     const timestamp = i["timestamp"];
  //     const devices_count = i["devices_count"];
  //     dataList.push({
  //       x: timestamp,
  //       y: devices_count
  //     })
  //   });

  //   // console.log(dataList);
  // }

  updateLiveChart(data: Data) {
    let chartToUpdate = 0;
    const isWifiData = data.sensor_type === "wifi";

    if (isWifiData) {
      chartToUpdate = 1;
    }

    // Append the new data to the existing chart data
    liveChart.data.datasets[chartToUpdate].data.push({
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
