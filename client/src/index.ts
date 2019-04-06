import { ChartHandler } from "./ChartHandler";
import { DataHandler } from "./DataHandler";
import { WebSocketHandler } from "./WebSocketHandler";

// Config 
const SERVER = "localhost"
const PORT = 8000

const SERVER_URL = `http://${SERVER}:${PORT}/data`;


window.onload = () => {
  const dataHandler = new DataHandler(SERVER_URL);
  // const chartHandler = new ChartHandler(dataHandler);
  // const wsHandler = new WebSocketHandler(WS_URL, chartHandler);

  // wsHandler.connect();
  // dataHandler.getLatest().then(data => chartHandler.initLiveChart(data));
  // dataHandler.getStats().then(data => chartHandler.initPieChart(data));
  // chartHandler.loopPieChartUpdate();

  let eventSource = new EventSource(`${SERVER_URL}/events`)
  eventSource.onmessage = (msg: MessageEvent) => {
    console.log("Got a Server-sent-event!");
    console.log(msg);

    // TODO: Convert to JSON?
    // let data = JSON.parse(msg.data);
    // console.log(data);

  };
};