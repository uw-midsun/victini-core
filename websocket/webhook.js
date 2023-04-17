const express = require("express");
var request = require("request");
const app = express();
const port = 3000;
var fs = require("fs");
const http = require("http");
const server = http.createServer(app);
const bodyParser = require("body-parser");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.get("/", (req, res) => {
  res.send("<h1>Data Page</h1>");
});

app.post("/", (req, res) => {
  let data = req.body;
  console.log("successfully received data from microservice");
  console.log(data);
  updateClient(data);
});

function updateClient(postData) {
  var clientServerOptions = {
    uri: "http://127.0.0.1:5000/input-data",
    body: JSON.stringify(postData),
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  };
  request(clientServerOptions, function (error, response) {
    console.log(error, response.body);
    return;
  });
}

const x = [1.1, 2, 3, 4];
const y = [4, 5, 2.2, 1];

function appendJSONtoFile(jsonFile, msData) {
  resData = "";
  fs.read(jsonFile, function (err, data) {
    var json = JSON.parse(data);
    json.push("search result: " + msData);
    resData = json;
    fs.writeFile(jsonFile, JSON.stringify());
  });
  return resData;
}

// const io = new Server(server);
const dummyData = {
  datas: {
    mode: "lines+markers",
    name: "Scatter",
    x: x,
    y: y,
  },
  layout: {
    title: "MSXV Data: ",
    x_axis_range: [1, 4],
    x_axis_title: "x",
    y_axis_range: [1, 5],
    y_axis_title: "y",
  },
};

server.listen(port, () => {
  console.log("server is listening on localhost" + port);
});
