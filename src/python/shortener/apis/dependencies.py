from fastapi import Request


async def get_uow(request: Request):
    return request.app.state.uow


async def get_publisher(request: Request):
    return request.app.state.publisher
