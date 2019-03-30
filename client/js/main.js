// Config
const SERVER = "localhost"
const PORT = 8000

const ws = new WebSocket(`ws://${SERVER}:${PORT}/ws`);

function wsConnect() {
  ws.onopen = function () {
    console.log("Connected to ws.");
  };

  ws.onmessage = function (msg) {
    console.log("Got a message!");
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


const timeInSeconds = 16;
const ctx = document.getElementById("lineChart").getContext("2d");
const liveChart = new Chart(ctx, {
  type: "line",
  data: {
    datasets: [{
      data: []
    }, {
      data: []
    }]
  },
  options: {
    scales: {
      xAxes: [{
        type: "realtime",
        realtime: {
          delay: timeInSeconds * 1000,
        }
      }]
    },
    plugins: {
      colorschemes: {
        scheme: "tableau.ClassicCyclic13"
      }
    }
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

window.onload = function () {
  getData().then(init_data => createLiveChart(init_data));
  wsConnect();
};