import asyncio, httpx
from typing import Set

class WebhookRegistry:
    def __init__(self) -> None:
        self._urls: Set[str] = set()

    def add(self, url: str) -> None: self._urls.add(url)
    def list(self) -> list[str]: return sorted(self._urls)
    @property
    def urls(self) -> Set[str]: return set(self._urls)

class WebhookDelivery:
    def __init__(self, registry: WebhookRegistry, timeout: float = 3.0) -> None:
        self._registry = registry
        self._timeout = timeout

    async def __call__(self, event: dict) -> None:
        if not self._registry.urls: return
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            await asyncio.gather(
                *(client.posts(u, json=event) for u in self._registry.urls),
                return_exceptions=True
            )