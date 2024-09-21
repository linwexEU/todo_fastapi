from aio_pika import connect_robust, ExchangeType, Message, DeliveryMode
from typing import Literal
from pydantic import EmailStr
from src.logger import config_logger
import logging


logger = logging.getLogger(__name__)
config_logger()


async def send_task(
    type_of_email: Literal["Create", "Delete"], employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str
) -> None:
    connection = await connect_robust("amqp://guest:guest@localhost")
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("email_exchange", ExchangeType.DIRECT)

        await exchange.publish(
            Message(
                body=f"{type_of_email}:{employee_email}:{employer_email}:{creator_name}:{task_name}".encode(),
                delivery_mode=DeliveryMode.PERSISTENT
            ),
            routing_key="email_queue"
        )

        if type_of_email == "Create":
            logger.info("Email was sent")
        else: 
            logger.info("Email was deleted")
