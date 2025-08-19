from app.domain.models import Device, DeviceCreate, DeviceUpdate
from app.domain.ports import DeviceRepository, EventPublisher

class DeviceService:
    def __init__(self, repo: DeviceRepository, events: EventPublisher) -> None:
        self._repo = repo
        self._events = events
        self._next_id = 1

    def list(self) -> list[Device]:
        return self._repo.list()

    def get(self, id: int) -> Device | None:
        return self._repo.get(id)

    async def create(self, body: DeviceCreate) -> Device:
        dev = Device(id=self._next_id, name=body.name, status="offline")
        self._next_id += 1
        self._repo.upsert(dev)
        await self._events.publish({"type": "device.created", "device": dev.model_dump()})
        return dev

    async def update(self, id: int, body: DeviceUpdate) -> Device:
        cur = self._repo.get(id)
        if not cur: raise KeyError("device not found")
        nxt = cur.model_copy(update=body.model_dump(exclude_unset=True))
        self._repo.upsert(nxt)
        await self._events.publish({"type": "device.updated", "device": nxt.model_dump()})
        return nxt

    async def delete(self, id: int) -> None:
        old = self._repo.delete(id)
        if old:
            await self._events.publish({"type": "device.deleted", "device": old.model_dump()})
