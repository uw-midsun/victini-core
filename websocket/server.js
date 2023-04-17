const express = require("express");
const app = express();
const port = 3000;
const http = require("http");
const server = http.createServer(app);

app.get("/", (req, res) => {
  res.send("<h1>Hello world</h1>");
});

const { Server } = require("socket.io");

const x = [1.1, 2, 3, 4];
const y = [4, 5, 2.2, 1];
const io = new Server(server);
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

// listening for connection to clients
io.on("connection", (socket) => {
  socket.emit("elevation_data", dummyData);
  console.log("let's goo");
});

server.listen(port, () => {
  console.log("server is listening on localhost" + port);
});
