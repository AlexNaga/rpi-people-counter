// Config
const SERVER = "localhost"
const PORT = 8000

const ws = new WebSocket(`ws://${SERVER}:${PORT}/ws`);

function wsConnect() {
  ws.onopen = function () {
    console.log("Connected to ws.");
  };

  ws.onmessage = function (msg) {
    const data = JSON.parse(msg.data);
    updateChart(data)
  };
}

async function getData() {
  const response = await fetch(`http://${SERVER}:${PORT}/data`)
  const data = await response.json()
  return data;
}

function updatePeopleCount(data) {
  const elem = document.getElementById("peopleCount");
  const peopleCount = data[0].devices_count;
  const text = `There"s approximately ${peopleCount} person in the area.`
  elem.textContent = text;
}


const delayInSeconds = 30 * 1000;
const ttlInSeconds = 90 * 1000;
const durationInSeconds = 40 * 1000;

const canvas: any = document.getElementById("lineChart");
const ctx = canvas.getContext("2d");
const liveChart = new Chart(ctx, {
  type: "line",
  data: {
    datasets: [{
      label: "Bluetooth",
      data: []
    }, {
      label: "WiFi",
      data: []
    }]
  },
  options: {
    title: {
      display: true,
      text: "Estimate of number of people in the area.",
    },
    scales: {
      xAxes: [{
        type: "realtime",
        realtime: {
          delay: delayInSeconds,
          duration: durationInSeconds,
          ttl: ttlInSeconds,
        }
      }],
      yAxes: [{
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


function createLiveChart(data) {
  const dataList = [];

  data.forEach(i => {
    const timestamp = i["timestamp"];
    const devices_count = i["devices_count"];
    dataList.push({
      x: timestamp,
      y: devices_count
    })
  });

  // console.log(dataList);
}

function updateChart(data) {
  console.log(data.timestamp);

  // Append the new data to the existing chart data
  liveChart.data.datasets[0].data.push({
    x: data.timestamp,
    y: data.devices_count
  });

  // Update chart datasets keeping the current animation
  liveChart.update({
    preservation: true
  });
}

function initChart() {
  let initDate = new Date();

  liveChart.data.datasets[0].data.push({
    x: initDate.setSeconds(initDate.getSeconds() - 30),
    y: 0
  });

  // Update chart datasets keeping the current animation
  liveChart.update({
    preservation: true
  });
  console.log("asd");

}

window.onload = function () {
  initChart();
  // getData().then(init_data => createLiveChart(init_data));
  wsConnect();
};