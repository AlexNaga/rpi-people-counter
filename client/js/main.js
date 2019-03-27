function main() {
    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onopen = function () {
        console.log("Connected to ws");
    };

    ws.onmessage = function (evt) {
        alert(evt.data);
    };
}

main();