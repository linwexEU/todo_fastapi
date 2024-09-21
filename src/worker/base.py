from abc import abstractmethod
from typing import Any
from src.store import BaseAccessor


class AbstractTaskAccessor(BaseAccessor):
    @abstractmethod
    async def send_email(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError
