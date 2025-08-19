from fastapi import FastAPI
from app.api.rest import rest_router
from app.api.websocket import ws_router
from app.api.graphql_api import make_graphql_router
from app.infrastructure.memory_repo import InMemoryDeviceRepo
from app.infrastructure.ws_connections import WebSocketHub
from app.infrastructure.webhook_delivery import WebhookRegistry, WebhookDelivery
from app.services.device_service import DeviceService
from app.services.event_bus import EventBus

def create_app() -> FastAPI:
    app = FastAPI(title="Tiny Sensor Hub")

    repo = InMemoryDeviceRepo()
    bus = EventBus()
    hub = WebSocketHub()
    hooks = WebhookRegistry()
    delivery = WebhookDelivery(hooks)

    # Wire observers (EventBus -> adapters)
    bus.subscribe(hub.broadcast)
    bus.subscribe(delivery)   # callable

    # Service depends on ports, not frameworks
    service = DeviceService(repo, bus)

    # Expose via app.state for DI
    app.state.device_service = service
    app.state.ws_hub = hub
    app.state.webhook_registry = hooks

    # Routers
    app.include_router(rest_router)
    app.include_router(ws_router)
    app.include_router(make_graphql_router(), prefix="/graphql")

    return app

app = create_app()
# Run: uvicorn app.main:app --reload
