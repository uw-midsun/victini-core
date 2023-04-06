import asyncio
import socketio
import websocket

def hello():
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:5000/trip_elevation")
    ws.send("Hello world!")


sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('I received a message!')
    hello()


async def main():
    await sio.connect('http://localhost:3000')
    await sio.wait()

if __name__ == "__main__":
    asyncio.run(main())

