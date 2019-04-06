import { ChartHandler } from "./ChartHandler";
import { Data } from "./DataInterface";

class EventHandler {
  private eventSource: EventSource;
  private chartHandler: ChartHandler;

  constructor(url: string, chartHandler: ChartHandler) {
    this.eventSource = new EventSource(url + "/events")
    this.chartHandler = chartHandler;
  }

  connect() {
    this.eventSource.onopen = this.onOpen;
    this.eventSource.onmessage = this.onMessage.bind(this);
  }

  private onOpen() {
    console.log("Connected to SSE.");
  }

  private onMessage(msg: MessageEvent) {
    const data: Data = JSON.parse(msg.data);
    this.chartHandler.updateLiveChart(data);
  }
}

export { EventHandler };