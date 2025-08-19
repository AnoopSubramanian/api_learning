from fastapi import APIRouter, Depends, HTTPException, Request
from app.domain.models import Device, DeviceCreate, DeviceUpdate, WebhookRegister
from app.infrastructure.webhook_delivery import WebhookRegistry
from app.services.device_service import DeviceService

rest_router = APIRouter()

def svc(req: Request) -> DeviceService:
    return req.app.state.device_service

def hooks(req: Request) -> WebhookRegistry:
    return req.app.state.webhook_registry

@rest_router.get("/devices", response_model=list[Device])
async def list_devices(s: DeviceService = Depends(svc)):
    return s.list()

@rest_router.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: int, s: DeviceService = Depends(svc)):
    d = s.get(device_id)
    if not d: raise HTTPException(404, "device not found")
    return d

@rest_router.post("/devices", response_model=Device, status_code=201)
async def create_device(body: DeviceCreate, s: DeviceService = Depends(svc)):
    return await s.create(body)

@rest_router.patch("/devices/{device_id}", response_model=Device)
async def update_device(device_id: int, body: DeviceUpdate, s: DeviceService = Depends(svc)):
    try:
        return await s.update(device_id, body)
    except KeyError:
        raise HTTPException(404, "device not found")

@rest_router.delete("/devices/{device_id}", status_code=204)
async def delete_device(device_id: int, s: DeviceService = Depends(svc)):
    await s.delete(device_id)
    return {"ok": True}

@rest_router.post("/webhooks", status_code=204)
async def register_webhook(body: WebhookRegister, r: WebhookRegistry = Depends(hooks)):
    r.add(str(body.url))
    return {"ok": True}

@rest_router.get("/webhooks", response_model=list[str])
async def list_webhooks(r: WebhookRegistry = Depends(hooks)):
    return r.list()
