from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractMessage
from src.email.send_email import send_create_email_about_new_task, send_create_email_about_delete_task
from src.logger import config_logger
import logging
import asyncio


logger = logging.getLogger(__name__)
config_logger()


async def start_consume() -> None:
    connection = await connect_robust("amqp://guest:guest@localhost")
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("email_exchange", ExchangeType.DIRECT)
        queue = await channel.declare_queue("email_queue", durable=True)

        await queue.bind(exchange)

        logger.info("[RabbitMQ] Start consuming...")

        async with queue.iterator() as iterator:
            message: AbstractMessage
            async for message in iterator:
                async with message.process():
                    type_of_email, employee_email, employer_email, creator_name, task_name = message.body.decode().split(":")

                    if type_of_email == "Create":
                        send_create_email_about_new_task(employee_email, employer_email, creator_name, task_name)
                    else:
                        send_create_email_about_delete_task(employee_email, employer_email, creator_name, task_name)

        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consume())
