import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Literal
from pydantic import EmailStr
from src.broker.send import send_task
from src.store import BaseAccessor, Store


class CoreAccessor(BaseAccessor):
    THREAD_COUNT = 3
    
    def __init__(self, store: Store) -> None:
        super().__init__(store)

        self._loop = asyncio.get_event_loop()
        self._thread_executor = ThreadPoolExecutor(max_workers=self.THREAD_COUNT)

    async def disconnect(self) -> None:
        self._thread_executor.shutdown(wait=True)

    async def send_email(self, type_of_email: Literal["Create", "Delete"], employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str) -> None:
        await send_task(type_of_email, employee_email, employer_email, creator_name, task_name)
