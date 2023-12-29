import asyncio
from typing import Callable

import aiogram
import aio_pika

from settings import USER, AMQP_URL


async def get_connection() -> aio_pika.abc.AbstractRobustConnection:
    connection = await aio_pika.connect_robust(AMQP_URL)
    return connection


async def bot_process(
        message: aio_pika.abc.AbstractIncomingMessage,
        bot: aiogram.Bot
) -> None:
    async with message.process():
        await bot.send_message(USER, message.body.decode('utf-8'))


async def socket_process(
        message: aio_pika.abc.AbstractIncomingMessage,
        writer: asyncio.StreamWriter
) -> None:
    async with message.process():
        writer.write(message.body)
        await writer.drain()


async def consume(
        connection: aio_pika.abc.AbstractRobustConnection,
        callback: Callable,
        queue_name: str,
) -> None:
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, auto_delete=True)
    await queue.consume(callback)


async def publish(
        connection: aio_pika.abc.AbstractRobustConnection,
        message: bytes,
        queue_name: str,
):
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(queue_name, auto_delete=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message),
            routing_key=queue_name,
        )
