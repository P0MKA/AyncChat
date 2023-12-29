import asyncio

BYTES_LENGTH = 2048   # количество байт, которое мы пытаемся получить из веб-сокета за раз
HOST = '89.104.67.139'  # ip сокет сервера
PORT = 8888  # порт сервера с сокетами


async def get_input(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)


async def receive(reader: asyncio.StreamReader):
    while '❤️ teisy':
        message = await reader.read(BYTES_LENGTH)
        if not message:
            break
        print(message.decode('utf-8'), end='\n-> ')


async def send(writer: asyncio.StreamWriter):
    while '❤️ teisy':
        message = await get_input('-> ')
        writer.write(message.encode('utf-8'))
        await writer.drain()


async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print('Здесь можно что-нибудь написать и отправить на сервер\nCTRL+C и Enter для выхода =)')

    incoming = asyncio.create_task(receive(reader))
    outgoing = asyncio.create_task(send(writer))

    await asyncio.gather(incoming, outgoing)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Пока-пока!')
