import logging

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shortener.adapters.orm import start_mappers
from shortener.adapters.publisher import Publisher
from shortener.apis import api_router
from shortener.apis.auth import secure_api_access
from shortener.config import settings
from shortener.services.unit_of_work import UnitOfWork

# TODO:
# 1. Done the auth in fastapi => just use basic auth for server, the user auth
#    will be handled by cockpit service
# 2. Always feature based, minimze refactoring and boilerplate
# 3. the short link is owned by user or team id

logger = logging.getLogger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    dependencies=[Depends(secure_api_access)],
)


@app.on_event("startup")
async def bootstrap(
    start_orm: bool = True,
    uow: UnitOfWork = UnitOfWork(),
    publisher: Publisher = Publisher(settings.PUBLISHER_DEST_HOST),
) -> None:
    if start_orm:
        start_mappers()

    app.state.uow: UnitOfWork = uow
    app.state.publisher: Publisher = await publisher.build()


app.include_router(
    api_router,
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level=settings.LOG_LEVEL.lower())
