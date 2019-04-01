import { ChartHandler } from "./ChartHandler";
import { Data } from "./DataInterface";

class WebSocketHandler {
  ws: WebSocket;

  constructor(url: string) {
    this.ws = new WebSocket(url);
  }

  connect() {
    this.ws.onopen = this.onOpen;
    this.ws.onmessage = this.onMessage;
  }

  private onOpen() {
    console.log("Connected to ws.");
  }

  onMessage(msg: MessageEvent) {
    const data: Data = JSON.parse(msg.data);
    const chartHandler = new ChartHandler();
    chartHandler.updateLiveChart(data);
  }
}

export { WebSocketHandler };