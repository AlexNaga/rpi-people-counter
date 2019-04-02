import { ChartHandler } from "./ChartHandler";
import { DataHandler } from "./DataHandler";
import { WebSocketHandler } from "./WebSocketHandler";

// Config 
const SERVER = "localhost"
const PORT = 8000

const SERVER_URL = `http://${SERVER}:${PORT}/data`;
const WS_URL = `ws://${SERVER}:${PORT}/ws`;


window.onload = () => {
  const chartHandler = new ChartHandler();
  const dataHandler = new DataHandler(SERVER_URL);
  const wsHandler = new WebSocketHandler(WS_URL, chartHandler);

  wsHandler.connect();
  dataHandler.getLatest().then(initData => chartHandler.initLiveChart(initData));
  dataHandler.getAllData().then(initData => chartHandler.initPieChart(initData));
};