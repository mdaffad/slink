from fastapi import Request
from shortener.adapters.publisher import Publisher
from shortener.services.unit_of_work import UnitOfWork


async def get_uow(request: Request) -> UnitOfWork:
    uow: UnitOfWork = request.app.state.uow
    return uow


async def get_publisher(request: Request) -> Publisher:
    publisher: Publisher = request.app.state.publisher
    return publisher
