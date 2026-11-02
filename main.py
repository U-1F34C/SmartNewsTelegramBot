import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from parsing import parse_news

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("bot token is not set. Please set the BOT_TOKEN environment variable.")

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Hello! I'm a news bot. I can provide you with the latest news updates. "
        "Use /news to get the latest news. Add me in your group to get news updates "
        "directly in your group chat!"
    )

@dp.message(Command("news"))
async def command_news_handler(message: Message) -> None:
    news = parse_news()[0]
    await message.answer(
        f"Title: {news['title']}\nLink: {news['link']}\nDescription: {news['description']}"
    )

@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text is None:
        return
    await message.answer(message.text)


async def main() -> None:
    bot = Bot(token=TOKEN)
    print("Bot started. Press Ctrl+C to stop.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())