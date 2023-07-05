from __future__ import annotations

import json

from aiokafka import AIOKafkaProducer
from shortener.domains.events import (
    ShortLinkCreated,
    ShortLinkDeleted,
    ShortLinkUpdated,
)


class Publisher:
    def __init__(self, dest_host: str) -> None:
        self.bootstrap_server: str = dest_host
        self.compression_type = "gzip"

    async def build(self) -> Publisher:
        self.producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            value_serializer=self.serializer,
            compression_type=self.compression_type,
        )
        await self.producer.start()
        return self

    def serializer(self, value):
        return json.dumps(value).encode()

    def update_cache(self, event: ShortLinkUpdated) -> None:
        # TODO: update dest link on cache
        self.producer.send(
            topic="UPDATE-CACHE",
            value={
                "source": event.source,
                "destination": event.destination,
                "is_private": event.is_private,
            },
        )

    async def create_cache(self, event: ShortLinkCreated) -> None:
        await self.producer.send(
            topic="CREATE-CACHE",
            value={
                "user_id": event.user_id,
                "source": event.source,
                "destination": event.destination,
                "is_private": event.is_private,
            },
        )

    async def invalidate_cache(self, event: ShortLinkDeleted) -> None:
        # TODO: invalidate removed short link on cache
        await self.producer.send(
            topic="INVALIDATE-CACHE",
            value={
                "source": event.source,
            },
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
