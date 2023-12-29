import asyncio

import aio_pika.abc

from rabbit import get_connection, socket_process, publish, consume
from settings import BYTES_LENGTH, HOST, PORT, BOT_QUEUE, SERVER_QUEUE


async def incoming(reader: asyncio.StreamReader):
    while True:
        line = await reader.read(BYTES_LENGTH)
        if not line:
            break

        connection = await get_connection()

        await publish(
            connection=connection,
            message=line,
            queue_name=BOT_QUEUE,
        )


async def outgoing(
        connection: aio_pika.abc.AbstractRobustConnection,
        writer: asyncio.StreamWriter,
):
    async def callback(message):
        await socket_process(message, writer)

    await consume(
        connection=connection,
        callback=callback,
        queue_name=SERVER_QUEUE
    )


async def handle_echo(reader, writer):
    connection = await get_connection()

    try:
        outgoing_task = asyncio.create_task(outgoing(connection, writer))
        incoming_task = asyncio.create_task(incoming(reader))

        await asyncio.gather(outgoing_task, incoming_task)

    except Exception:
        pass

    finally:
        writer.close()
        await writer.wait_closed()
        await connection.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, HOST, PORT)

    address = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {address}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
