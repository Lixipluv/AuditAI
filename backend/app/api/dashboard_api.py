from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["Dashboard"])
connections = []

@router.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.remove(websocket)

async def broadcast_dashboard_update(data):
    for conn in connections:
        await conn.send_json(data)
