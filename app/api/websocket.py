from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from app.infrastructure.ws_connections import WebSocketHub

ws_router = APIRouter()

def hub(req: Request) -> WebSocketHub:
    return req.app.state.ws_hub

@ws_router.websocket("/ws/updates")
async def ws_updates(ws: WebSocket, req: Request):
    h = hub(req)
    await h.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keepalive
    except WebSocketDisconnect:
        h.disconnect(ws)
