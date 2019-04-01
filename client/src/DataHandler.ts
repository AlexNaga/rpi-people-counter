class DataHandler {
  url: string;

  constructor(url: string) {
    this.url = url;
  }

  async getAllData() {
    const response = await fetch(this.url + "/all");
    const data = await response.json();
    return data;
  }

  async getAllBtData() {
    const response = await fetch(this.url + "/all/bt");
    const data = await response.json();
    return data;
  }

  async getAllWifiData() {
    const response = await fetch(this.url + "/all/wifi");
    const data = await response.json();
    return data;
  }

  async getLatest() {
    const response = await fetch(this.url + "/latest");
    const data = await response.json();
    return data;
  }

  async getLatestBt() {
    const response = await fetch(this.url + "/latest/bt");
    const data = await response.json();
    return data;
  }

  async getLatestWifi() {
    const response = await fetch(this.url + "/latest/wifi");
    const data = await response.json();
    return data;
  }
}

export { DataHandler };