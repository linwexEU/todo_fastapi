from typing import Literal
from pydantic import EmailStr
from src.store import Store
from starlette.background import BackgroundTask
from src.worker.async_celery.accessor import AsyncCeleryTaskAccessor
from src.worker.base import AbstractTaskAccessor


class WorkerAccessor(AbstractTaskAccessor):
    def __init__(self, store: Store) -> None:
        super().__init__(store)

        self.async_celery = AsyncCeleryTaskAccessor(store)

    async def connect(self) -> None:
        self.logger.info("Connecting to workers")
        await self.async_celery.connect()
        self.logger.info("Connected to workers")

    async def disconnect(self) -> None:
        self.logger.info("Disconnecting from workers")
        await self.async_celery.disconnect()
        self.logger.info("Disconnected form workers")

    async def send_email(self, type_of_email: Literal["Create", "Delete"], employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str):
        await self.async_celery.send_email(type_of_email, employee_email, employer_email, creator_name, task_name)
