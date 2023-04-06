const express = require("express");
const app = express();
const port = 3000;
const http = require("http");
const server = http.createServer(app);

app.get("/", (req, res) => {
  res.send("<h1>Hello world</h1>");
});

const { Server } = require("socket.io");

const io = new Server(server);

// listening for connection to clients
io.on("connection", (socket) => {
  socket.emit("welcome", "cool stuff");
  console.log("let's goo");
});

server.listen(port, () => {
  console.log("server is listening on localhost" + port);
});
