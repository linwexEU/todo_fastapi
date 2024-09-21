from src.store import get_store
from src.worker.async_celery.app import async_celery_app
from typing import Literal
from pydantic import EmailStr


@async_celery_app.task
async def send_email(type_of_email: Literal["Create", "Delete"], employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str) -> None:
    store = get_store()
    return await store.core.send_email(type_of_email, employee_email, employer_email, creator_name, task_name)
