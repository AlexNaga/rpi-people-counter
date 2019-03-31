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
  const wsHandler = new WebSocketHandler(WS_URL);

  // dataHandler.getData().then(init_data => chartHandler.createLiveChart(init_data));
  wsHandler.connect();
};