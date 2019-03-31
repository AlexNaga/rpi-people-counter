class DataHandler {
  url: string;

  constructor(url: string) {
    this.url = url;
  }

  async getData() {
    const response = await fetch(this.url);
    const data = await response.json();
    return data;
  }
}

export { DataHandler };