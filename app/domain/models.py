from pydantic import BaseModel, HttpUrl
from typing import Optional

class Device(BaseModel):
    id: int
    name: str
    status: str = "offline"
    metric: float | None = None

class DeviceCreate(BaseModel):
    name: str

class DeviceUpdate(BaseModel):
    status: str | None = None
    metric: float | None = None
    name: str | None = None

class WebhookRegister(BaseModel):
    url: HttpUrl
