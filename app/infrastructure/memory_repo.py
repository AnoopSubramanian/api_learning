from typing import Dict
from app.domain.models import Device
from app.domain.ports import DeviceRepository

class InMemoryDeviceRepo(DeviceRepository):
    def __init__(self) -> None:
        self._items: Dict[int, Device] = {}

    def list(self) -> list[Device]:
        return list(self._items.values())

    def get(self, id: int) -> Device | None:
        return self._items.get(id)

    def upsert(self, device: Device) -> Device:
        self._items[device.id] = device
        return device

    def delete(self, id: int) -> Device | None:
        return self._items.pop(id, None)
