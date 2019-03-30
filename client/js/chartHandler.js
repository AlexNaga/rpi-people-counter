function updateChart(data) {
  const lineChart = document.getElementById("lineChart");
  const newLineChart = new Chart(lineChart, {
    type: "line",
    data: chartData,
    options: options
  });

  newLineChart.update();
}



