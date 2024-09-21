from enum import Enum


class TaskWorkerEnum(str, Enum):
    async_celery = "async-celery"
