from typing import Literal

import arq
import arq.connections
from pydantic import EmailStr


async def send_email(
    ctx: dict, type_of_email: Literal["Create", "Delete"], employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str
) -> None:
    pass 










