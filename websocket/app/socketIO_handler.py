import asyncio
import socketio
import websocket
import json

def send_data(data):
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:5000/test")
    ws.send(data)


sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('Connection Established')


@sio.on('elevation_data')
async def on_elevation_data(data):
    print('Data Received')
    print(data)
    send_data(json.dumps(data))

async def main():
    await sio.connect('http://localhost:3000')
    await sio.wait()

if __name__ == "__main__":
    asyncio.run(main())

