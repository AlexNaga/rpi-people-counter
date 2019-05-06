import { ChartHandler } from "./ChartHandler";
import { DataHandler } from "./DataHandler";
import { EventHandler } from "./EventHandler";

// Config
// const SERVER = "localhost";
const SERVER = "rpi-counter.local";
const PORT = 8000;

const SERVER_URL = `http://${SERVER}:${PORT}/data`;

window.onload = () => {
  const dataHandler = new DataHandler(SERVER_URL);
  const chartHandler = new ChartHandler(dataHandler);
  const eventHandler = new EventHandler(SERVER_URL, chartHandler);

  eventHandler.connect();
  dataHandler.getLatest().then(data => chartHandler.initLiveChart(data));
  dataHandler.getStats().then(data => chartHandler.initPieChart(data));
  chartHandler.loopPieChartUpdate();
};
