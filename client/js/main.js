// Config
const WS_SERVER = "localhost"
const WS_PORT = 8000

function wsConnect() {
    const ws = new WebSocket(`ws://${WS_SERVER}:${WS_PORT}/ws`);
    ws.onopen = function () {
        console.log('Connected to ws');
    };

    ws.onmessage = function (msg) {
        console.log(msg);
    };
}

function main() {
    wsConnect();
}

main();