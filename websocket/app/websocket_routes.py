import asyncio
import json
import random
from quart import websocket, Quart
import requests
import pandas as pd
import plotly
import plotly.graph_objects as go
import csv
import socketio


app = Quart(__name__)
csv_dir = "./sample_route_step4.csv"

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('I received a message!')

async def main():
    await sio.connect('http://localhost:3000')
    await sio.wait()

@app.websocket("/trip_elevation")
async def update_graph_scatter_elevation():
    data = json.dumps(update_graph_scatter("trip_elevation.csv", "trip(m)", "elevation(m)"))
    print(type(data))
    await websocket.send(data)
    await asyncio.sleep(5)


@app.websocket("/trip_distance")
async def update_graph_scatter_distance():
    data = await websocket.receive()
    print(data)
    data = json.dumps(update_graph_scatter("trip_distance.csv", "trip(m)", "dist_to_next_coordinate(m)"))
    await websocket.send(data)
    await asyncio.sleep(5)

@app.websocket("/trip_latitude")
async def update_graph_scatter_latitude():
    data = json.dumps(update_graph_scatter("trip_latitude.csv", "trip(m)", "latitude"))
    await websocket.send(data)
    await asyncio.sleep(5)

@app.websocket("/trip_longitude")
async def update_graph_scatter_longitude():
    data = json.dumps(update_graph_scatter("trip_longitude.csv", "trip(m)", "longitude"))
    await websocket.send(data)
    await asyncio.sleep(5)


def update_graph_scatter(name, x_axis, y_axis):
    df = pd.read_csv(name, on_bad_lines='skip')
    data = {"datas": {
    'mode': 'lines+markers',
    'name': 'Scatter',
     'x' : df[x_axis].to_list(), # [20, 30 ,40]
     'y' : df[y_axis].to_list(),
        },
    "layout": {'title': "MSXV Data: " + str(x_axis) + "-" + str(y_axis), 'x_axis_range': [min(df[x_axis]), max(df[x_axis])],
                'x_axis_title': x_axis, 'y_axis_range': [min(df[y_axis]), max(df[y_axis])],
                'y_axis_title': y_axis,}  }

    return data


if __name__ == "__main__":
    app.run(port=5000)
    asyncio.run(main())