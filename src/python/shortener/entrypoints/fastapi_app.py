import logging

import uvicorn
from fastapi import FastAPI
from shortener.adapters.orm import start_mappers
from shortener.apis import api_router
from shortener.config import settings

# TODO:
# 1. Done the auth in fastapi => just use basic auth for server, the user auth
#    will be handled by cockpit service
# 2. Always feature based, minimze refactoring and boilerplate
# 3. the short link is owned by user or team id

logger = logging.getLogger()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)


@app.on_event("startup")
async def bootstrap() -> None:
    start_mappers()


app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="debug")
