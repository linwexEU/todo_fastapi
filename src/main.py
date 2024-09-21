from fastapi import FastAPI
from src.store import store_lifespan
from fastapi.middleware import Middleware
from src.api.routers import all_routers
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from src.config import settings
from src.utils.middleware import AuthTimeMiddleware
from src.broker.receive import start_consume
import asyncio
import uvicorn


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with store_lifespan():
        redis = aioredis.from_url(settings.REDIS_URL)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        task = asyncio.create_task(start_consume())
        yield
        task.cancel()
        await task


def init_routers(app: FastAPI, routers) -> None:
    for router in routers:
        app.include_router(router)


def init_middleware() -> list[Middleware]:
    return [Middleware(AuthTimeMiddleware)]


def create_app() -> FastAPI:
    app = FastAPI(title="ToDo📋", lifespan=lifespan, middleware=init_middleware())
    init_routers(app, all_routers)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
