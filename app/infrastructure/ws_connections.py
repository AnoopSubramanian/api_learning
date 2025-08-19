from typing import Set
from fastapi import WebSocket

class WebsocketHub:
    def __init__(self) -> None:
        self._conns: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._conns.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self._conns.discard(ws)

    async def broadcast(self, event: dict) -> None:
        dead = []
        for ws in list(self._conns):
            try:
                await ws.send_json(event)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._conns.discard(ws)
