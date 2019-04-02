import { ChartHandler } from "./ChartHandler";
import { DataHandler } from "./DataHandler";
import { WebSocketHandler } from "./WebSocketHandler";

// Config 
const SERVER = "localhost"
const PORT = 8000

const SERVER_URL = `http://${SERVER}:${PORT}/data`;
const WS_URL = `ws://${SERVER}:${PORT}/ws`;


function sleep(seconds: number) {
  seconds = seconds * 1000;
  return new Promise(resolve => setTimeout(resolve, seconds));
}

async function loopPieChartUpdate(dataHandler: DataHandler, chartHandler: ChartHandler) {
  dataHandler.getStats().then(stats => chartHandler.updatePieChart(stats));
  await sleep(5);
  loopPieChartUpdate(dataHandler, chartHandler) // Recursive call
}


window.onload = () => {
  const chartHandler = new ChartHandler();
  const dataHandler = new DataHandler(SERVER_URL);
  const wsHandler = new WebSocketHandler(WS_URL, chartHandler);

  wsHandler.connect();
  dataHandler.getLatest().then(data => chartHandler.initLiveChart(data));
  dataHandler.getStats().then(data => chartHandler.initPieChart(data));
  loopPieChartUpdate(dataHandler, chartHandler);
};