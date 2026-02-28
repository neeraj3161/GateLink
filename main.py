from fastapi import FastAPI,Body, WebSocket, WebSocketDisconnect
import asyncio

from starlette.middleware.base import BodyStreamGenerator

app = FastAPI()

connected_clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client Connected")

    connected_clients.append(websocket)

    try:
        while True:
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        print("Client Disconnected")
        if websocket in connected_clients:
            connected_clients.remove(websocket)


@app.post("/open-gate")
async def open_gate():
    dead_clients = []

    for client in connected_clients:
        try:
            await client.send_text("OPEN")
        except:
            dead_clients.append(client)

    # Remove broken sockets
    for dead in dead_clients:
        connected_clients.remove(dead)

    return {"status": "sent"}


@app.post("/gate-open-log")
async def log_gate(log:str= Body(...) ):
    # send this log to telegram later
    print(log)
    return {'log': log}