import asyncio

from aiokafka import AIOKafkaConsumer


async def start_consumer():
    consumer = AIOKafkaConsumer("CREATE-CACHE", bootstrap_servers="localhost:9092")
    await consumer.start()
    try:
        async for msg in consumer:
            print("coy")
            print(
                "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
            )
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(start_consumer())
