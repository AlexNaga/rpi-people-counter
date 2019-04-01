/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/index.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/ChartHandler.ts":
/*!*****************************!*\
  !*** ./src/ChartHandler.ts ***!
  \*****************************/
/*! exports provided: ChartHandler */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"ChartHandler\", function() { return ChartHandler; });\n// Config\nvar delayInSeconds = 30 * 1000;\nvar ttlInSeconds = 90 * 1000;\nvar durationInSeconds = 40 * 1000;\nvar canvas = document.getElementById(\"liveChart\");\nvar ctx = canvas.getContext(\"2d\");\nvar liveChart = new Chart(ctx, {\n    type: \"line\",\n    data: {\n        datasets: [{\n                label: \"Bluetooth\",\n                data: [],\n                fill: false\n            }, {\n                label: \"WiFi\",\n                data: [],\n                fill: false\n            }]\n    },\n    options: {\n        title: {\n            display: true,\n            text: \"Estimate of number of people in the area.\",\n        },\n        scales: {\n            xAxes: [{\n                    type: \"realtime\",\n                    realtime: {\n                        delay: delayInSeconds,\n                        duration: durationInSeconds,\n                        ttl: ttlInSeconds,\n                    }\n                }],\n            yAxes: [{\n                    ticks: {\n                        beginAtZero: true,\n                        callback: function (value) { if (value % 1 === 0) {\n                            return value;\n                        } },\n                        suggestedMax: 10,\n                        suggestedMin: 0,\n                    }\n                }]\n        },\n        plugins: {\n            colorschemes: {\n                scheme: \"tableau.ClassicCyclic13\"\n            }\n        },\n    }\n});\nvar ChartHandler = /** @class */ (function () {\n    function ChartHandler() {\n    }\n    ChartHandler.prototype.initLiveChart = function (data) {\n        var initDate = new Date();\n        var delayTime = [[30, 5], [5, 5]];\n        for (var i = 0; i < data.length; i++) {\n            liveChart.data.datasets[i].data.push({\n                x: initDate.setSeconds(initDate.getSeconds() - delayTime[i][0]),\n                y: data[i].devices_count\n            });\n            liveChart.data.datasets[i].data.push({\n                x: initDate.setSeconds(initDate.getSeconds() + delayTime[i][1]),\n                y: data[i].devices_count\n            });\n        }\n        // Update chart datasets keeping the current animation\n        liveChart.update({\n            preservation: true\n        });\n    };\n    // createLiveChart(data) {\n    //   const dataList = [];\n    //   data.forEach(i => {\n    //     const timestamp = i[\"timestamp\"];\n    //     const devices_count = i[\"devices_count\"];\n    //     dataList.push({\n    //       x: timestamp,\n    //       y: devices_count\n    //     })\n    //   });\n    //   // console.log(dataList);\n    // }\n    ChartHandler.prototype.updateLiveChart = function (data) {\n        var chartToUpdate = 0;\n        var isWifiData = data.sensor_type === \"wifi\";\n        if (isWifiData) {\n            chartToUpdate = 1;\n        }\n        // Append the new data to the existing chart data\n        liveChart.data.datasets[chartToUpdate].data.push({\n            x: data.timestamp,\n            y: data.devices_count\n        });\n        // Update chart datasets keeping the current animation\n        liveChart.update({\n            preservation: true\n        });\n    };\n    return ChartHandler;\n}());\n\n\n\n//# sourceURL=webpack:///./src/ChartHandler.ts?");

/***/ }),

/***/ "./src/DataHandler.ts":
/*!****************************!*\
  !*** ./src/DataHandler.ts ***!
  \****************************/
/*! exports provided: DataHandler */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"DataHandler\", function() { return DataHandler; });\nvar __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {\n    return new (P || (P = Promise))(function (resolve, reject) {\n        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }\n        function rejected(value) { try { step(generator[\"throw\"](value)); } catch (e) { reject(e); } }\n        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }\n        step((generator = generator.apply(thisArg, _arguments || [])).next());\n    });\n};\nvar __generator = (undefined && undefined.__generator) || function (thisArg, body) {\n    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;\n    return g = { next: verb(0), \"throw\": verb(1), \"return\": verb(2) }, typeof Symbol === \"function\" && (g[Symbol.iterator] = function() { return this; }), g;\n    function verb(n) { return function (v) { return step([n, v]); }; }\n    function step(op) {\n        if (f) throw new TypeError(\"Generator is already executing.\");\n        while (_) try {\n            if (f = 1, y && (t = op[0] & 2 ? y[\"return\"] : op[0] ? y[\"throw\"] || ((t = y[\"return\"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;\n            if (y = 0, t) op = [op[0] & 2, t.value];\n            switch (op[0]) {\n                case 0: case 1: t = op; break;\n                case 4: _.label++; return { value: op[1], done: false };\n                case 5: _.label++; y = op[1]; op = [0]; continue;\n                case 7: op = _.ops.pop(); _.trys.pop(); continue;\n                default:\n                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }\n                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }\n                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }\n                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }\n                    if (t[2]) _.ops.pop();\n                    _.trys.pop(); continue;\n            }\n            op = body.call(thisArg, _);\n        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }\n        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };\n    }\n};\nvar DataHandler = /** @class */ (function () {\n    function DataHandler(url) {\n        this.url = url;\n    }\n    DataHandler.prototype.getAllData = function () {\n        return __awaiter(this, void 0, void 0, function () {\n            var response, data;\n            return __generator(this, function (_a) {\n                switch (_a.label) {\n                    case 0: return [4 /*yield*/, fetch(this.url + \"/all\")];\n                    case 1:\n                        response = _a.sent();\n                        return [4 /*yield*/, response.json()];\n                    case 2:\n                        data = _a.sent();\n                        return [2 /*return*/, data];\n                }\n            });\n        });\n    };\n    DataHandler.prototype.getAllBtData = function () {\n        return __awaiter(this, void 0, void 0, function () {\n            var response, data;\n            return __generator(this, function (_a) {\n                switch (_a.label) {\n                    case 0: return [4 /*yield*/, fetch(this.url + \"/all/bt\")];\n                    case 1:\n                        response = _a.sent();\n                        return [4 /*yield*/, response.json()];\n                    case 2:\n                        data = _a.sent();\n                        return [2 /*return*/, data];\n                }\n            });\n        });\n    };\n    DataHandler.prototype.getAllWifiData = function () {\n        return __awaiter(this, void 0, void 0, function () {\n            var response, data;\n            return __generator(this, function (_a) {\n                switch (_a.label) {\n                    case 0: return [4 /*yield*/, fetch(this.url + \"/all/wifi\")];\n                    case 1:\n                        response = _a.sent();\n                        return [4 /*yield*/, response.json()];\n                    case 2:\n                        data = _a.sent();\n                        return [2 /*return*/, data];\n                }\n            });\n        });\n    };\n    DataHandler.prototype.getLatest = function () {\n        return __awaiter(this, void 0, void 0, function () {\n            var response, data;\n            return __generator(this, function (_a) {\n                switch (_a.label) {\n                    case 0: return [4 /*yield*/, fetch(this.url + \"/latest\")];\n                    case 1:\n                        response = _a.sent();\n                        return [4 /*yield*/, response.json()];\n                    case 2:\n                        data = _a.sent();\n                        return [2 /*return*/, data];\n                }\n            });\n        });\n    };\n    DataHandler.prototype.getLatestBt = function () {\n        return __awaiter(this, void 0, void 0, function () {\n            var response, data;\n            return __generator(this, function (_a) {\n                switch (_a.label) {\n                    case 0: return [4 /*yield*/, fetch(this.url + \"/latest/bt\")];\n                    case 1:\n                        response = _a.sent();\n                        return [4 /*yield*/, response.json()];\n                    case 2:\n                        data = _a.sent();\n                        return [2 /*return*/, data];\n                }\n            });\n        });\n    };\n    DataHandler.prototype.getLatestWifi = function () {\n        return __awaiter(this, void 0, void 0, function () {\n            var response, data;\n            return __generator(this, function (_a) {\n                switch (_a.label) {\n                    case 0: return [4 /*yield*/, fetch(this.url + \"/latest/wifi\")];\n                    case 1:\n                        response = _a.sent();\n                        return [4 /*yield*/, response.json()];\n                    case 2:\n                        data = _a.sent();\n                        return [2 /*return*/, data];\n                }\n            });\n        });\n    };\n    return DataHandler;\n}());\n\n\n\n//# sourceURL=webpack:///./src/DataHandler.ts?");

/***/ }),

/***/ "./src/WebSocketHandler.ts":
/*!*********************************!*\
  !*** ./src/WebSocketHandler.ts ***!
  \*********************************/
/*! exports provided: WebSocketHandler */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"WebSocketHandler\", function() { return WebSocketHandler; });\n/* harmony import */ var _ChartHandler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ChartHandler */ \"./src/ChartHandler.ts\");\n\nvar WebSocketHandler = /** @class */ (function () {\n    function WebSocketHandler(url) {\n        this.ws = new WebSocket(url);\n    }\n    WebSocketHandler.prototype.connect = function () {\n        this.ws.onopen = this.onOpen;\n        this.ws.onmessage = this.onMessage;\n    };\n    WebSocketHandler.prototype.onOpen = function () {\n        console.log(\"Connected to ws.\");\n    };\n    WebSocketHandler.prototype.onMessage = function (msg) {\n        var data = JSON.parse(msg.data);\n        var chartHandler = new _ChartHandler__WEBPACK_IMPORTED_MODULE_0__[\"ChartHandler\"]();\n        chartHandler.updateLiveChart(data);\n    };\n    return WebSocketHandler;\n}());\n\n\n\n//# sourceURL=webpack:///./src/WebSocketHandler.ts?");

/***/ }),

/***/ "./src/index.ts":
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _ChartHandler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ChartHandler */ \"./src/ChartHandler.ts\");\n/* harmony import */ var _DataHandler__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./DataHandler */ \"./src/DataHandler.ts\");\n/* harmony import */ var _WebSocketHandler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./WebSocketHandler */ \"./src/WebSocketHandler.ts\");\n\n\n\n// Config \nvar SERVER = \"localhost\";\nvar PORT = 8000;\nvar SERVER_URL = \"http://\" + SERVER + \":\" + PORT + \"/data\";\nvar WS_URL = \"ws://\" + SERVER + \":\" + PORT + \"/ws\";\nwindow.onload = function () {\n    var chartHandler = new _ChartHandler__WEBPACK_IMPORTED_MODULE_0__[\"ChartHandler\"]();\n    var dataHandler = new _DataHandler__WEBPACK_IMPORTED_MODULE_1__[\"DataHandler\"](SERVER_URL);\n    var wsHandler = new _WebSocketHandler__WEBPACK_IMPORTED_MODULE_2__[\"WebSocketHandler\"](WS_URL);\n    wsHandler.connect();\n    dataHandler.getLatest().then(function (init_data) { return chartHandler.initLiveChart(init_data); });\n};\n\n\n//# sourceURL=webpack:///./src/index.ts?");

/***/ })

/******/ });