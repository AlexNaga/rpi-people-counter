// Config
const SERVER = "localhost"
const PORT = 8000

const ws = new WebSocket(`ws://${SERVER}:${PORT}/ws`);

function wsConnect() {
    ws.onopen = function () {
        console.log('Connected to ws');
    };

    ws.onmessage = function (msg) {
        console.log(msg);
    };
}

function getData() {
    fetch(`http://${SERVER}:${PORT}/data`)
        .then(function (response) {
            return response.json();
        })
        .then(function (json_data) {
            console.log(json_data);
        });
}
function main() {
    getData();
    wsConnect();
}

main();