from __future__ import annotations

import json

from aiokafka import AIOKafkaProducer
from pydantic import AnyUrl

# async def produce():
#     producer = AIOKafkaProducer(
#         bootstrap_servers='localhost:9092',
#         value_serializer=serializer,
#         compression_type="gzip")

#     await producer.start()
#     data = {"a": 123.4, "b": "some string"}
#     await producer.send('foobar', data)
#     data = [1,2,3,4]
#     await producer.send('foobar', data)
#     await producer.stop()


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

    def serializer(self, value):
        return json.dumps(value).encode()

    def update_cache() -> None:
        # TODO: update dest link on cache
        return

    def invalidate_cache() -> None:
        # TODO: invalidate removed short link on cache
        return

    async def __aenter__(self):
        self.start_repository_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
