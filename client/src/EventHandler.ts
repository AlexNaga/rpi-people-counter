import { ChartHandler } from "./ChartHandler";
import { Data } from "./DataInterface";

class EventHandler {
  private eventSource: EventSource;
  private chartHandler: ChartHandler;
  private tmpList = [];

  constructor(url: string, chartHandler: ChartHandler) {
    this.eventSource = new EventSource(url + "/sse");
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

    this.tmpList.push(data);
    let isTwoItems = this.tmpList.length === 2;

    if (isTwoItems) {
      this.chartHandler.updateBarChart(this.tmpList);
      this.chartHandler.updatePeopleEstimate(this.tmpList);
      this.tmpList = [];
    }
  }
}

export { EventHandler };
