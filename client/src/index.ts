import { ChartHandler } from "./ChartHandler";
import { DataHandler } from "./DataHandler";
import { WebSocketHandler } from "./WebSocketHandler";

// Config 
const SERVER = "localhost"
const PORT = 8000

const SERVER_URL = `http://${SERVER}:${PORT}/data`;
const WS_URL = `ws://${SERVER}:${PORT}/ws`;


window.onload = () => {
  const dataHandler = new DataHandler(SERVER_URL);
  const chartHandler = new ChartHandler(dataHandler);
  const wsHandler = new WebSocketHandler(WS_URL, chartHandler);

  wsHandler.connect();
  dataHandler.getLatest().then(data => chartHandler.initLiveChart(data));
  dataHandler.getStats().then(data => chartHandler.initPieChart(data));
  chartHandler.loopPieChartUpdate();
};