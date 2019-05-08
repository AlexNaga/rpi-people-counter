import { ChartHandler } from "./ChartHandler";
import { DataHandler } from "./DataHandler";
import { EventHandler } from "./EventHandler";

const config = require("../config/config.json");
const SERVER = config.SERVER;
const PORT = config.PORT;

const SERVER_URL = `http://${SERVER}:${PORT}`;

window.onload = () => {
  const dataHandler = new DataHandler(SERVER_URL);
  const chartHandler = new ChartHandler(dataHandler);
  const eventHandler = new EventHandler(SERVER_URL, chartHandler);

  eventHandler.connect();
  dataHandler.getLatest()
    .then(data => chartHandler.initLiveChart(data))
    .catch(e => console.log("Could not fetch latest data."))

  dataHandler.getStats()
    .then(data => chartHandler.initPieChart(data))
    // .catch(e => console.log("Could not fetch statistics."));
    .catch(e => console.log(e));

  chartHandler.loopPieChartUpdate();
};
