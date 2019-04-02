import { ChartHandler } from "./ChartHandler";
import { Data } from "./DataInterface";

class WebSocketHandler {
  private ws: WebSocket;
  private chartHandler: ChartHandler;

  constructor(url: string, chartHandler: ChartHandler) {
    this.ws = new WebSocket(url);
    this.chartHandler = chartHandler;
  }

  connect() {
    this.ws.onopen = this.onOpen;
    this.ws.onmessage = this.onMessage.bind(this);
  }

  private onOpen() {
    console.log("Connected to ws.");
  }

  private onMessage(msg: MessageEvent) {
    const data: Data = JSON.parse(msg.data);
    this.chartHandler.updateLiveChart(data);
  }
}

export { WebSocketHandler };