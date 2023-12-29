import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from rabbit import get_connection, publish, bot_process, consume
from settings import TOKEN, BOT_QUEUE, SERVER_QUEUE


dp = Dispatcher()


@dp.message()
async def echo_handler(message: types.Message) -> None:
    connection = await get_connection()
    await publish(
        connection=connection,
        message=message.text.encode('utf-8'),
        queue_name=SERVER_QUEUE,
    )


async def outgoing(bot: Bot):
    async def callback(message):
        await bot_process(message, bot)

    connection = await get_connection()

    await consume(
        connection=connection,
        callback=callback,
        queue_name=BOT_QUEUE
    )


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    polling = asyncio.create_task(dp.start_polling(bot, skip_updates=True))
    consuming = asyncio.create_task(outgoing(bot))

    await asyncio.gather(polling, consuming)


if __name__ == "__main__":
    asyncio.run(main())
