from __future__ import annotations

import json

from aiokafka import AIOKafkaProducer
from pydantic import AnyUrl
from shortener.domains.models import ShortLink


class Publisher:
    def __init__(self, dest_host: AnyUrl) -> None:
        self.bootstrap_server: AnyUrl = dest_host
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

    def update_cache(self, short_link: ShortLink) -> None:
        # TODO: update dest link on cache
        self.producer.send(
            topic="UPDATE-CACHE",
            value={
                "source": short_link.source,
                "destination": short_link.destination,
                "is_private": short_link.is_private,
            },
        )

    def invalidate_cache(self, short_link: ShortLink) -> None:
        # TODO: invalidate removed short link on cache
        self.producer.send(
            topic="INVALIDATE-CACHE",
            value={
                "source": short_link.source,
            },
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
