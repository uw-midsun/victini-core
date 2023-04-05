const express = require("express");
const app = express();
const port = 3000;
const http = require("http").createServer();

const io = require("socket.io")(http);

// listening for connection to clients
io.on("connection", (socket) => {
  socket.emit("welcome", "cool stuff");
  console.log("let's goo");
});

http.listen(port, () => {
  console.log("server is listening on localhost" + port);
});
