from src.common.enums import TaskWorkerEnum
from src.worker.async_celery.tasks import send_email
from src.worker.base import AbstractTaskAccessor
from typing import Literal
from pydantic import EmailStr


class AsyncCeleryTaskAccessor(AbstractTaskAccessor):
    KEY = TaskWorkerEnum.async_celery.value

    async def send_email(self, type_of_email: Literal["Create", "Delete"], employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str) -> None:
        send_email.delay(self.KEY, type_of_email=type_of_email, employee_email=employee_email, employer_email=employer_email, creator_name=creator_name, task_name=task_name)
