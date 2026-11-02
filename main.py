# Загрузка необходимых библиотек и модулей
import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from parsing import get_news, parse_news

# Загрузка переменных окружения из файла .env
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

SUBSCRIBERS = set() 

# Проверка наличия токена бота
if not TOKEN:
    raise RuntimeError("bot token is not set. Please set the BOT_TOKEN environment variable.")

# Инициализация бота и диспетчера
dp = Dispatcher()
bot = Bot(token=TOKEN)

# Функция для создания текстового сообщения из данных новости
def create_text_message(news_data: dict) -> str:
    return (
        f"{news_data['title']}\n\n"
        f"{news_data['description']}\n"
        f"{news_data['link']}"
    )

# Асинхронная функция для периодического парсинга новостей и отправки их подписчикам
async def scheduler():
    while True:
        news = await parse_news()

        if not (news["status"] and news["message"] == "Success"):
            await asyncio.sleep(120)
            continue

        text = create_text_message(news["data"])

        for chat_id in list(SUBSCRIBERS):
            await bot.send_message(chat_id=chat_id, text=text)

        await asyncio.sleep(120)


# Обработчик команды /start
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Hello! I'm a news bot. I can provide you with the latest news updates. "
        "Use /news to get the latest news. Add me in your group to get news updates "
        "directly in your group chat!"
    )

# Обработчик команды /subscribe
@dp.message(Command("subscribe"))
async def command_subscribe_handler(message: Message) -> None:
    SUBSCRIBERS.add(message.chat.id)
    await message.answer("You have subscribed to news updates.")

# Обработчик команды /unsubscribe
@dp.message(Command("unsubscribe"))
async def command_unsubscribe_handler(message: Message) -> None:
    SUBSCRIBERS.discard(message.chat.id)
    await message.answer("You have unsubscribed from news updates.")


# Обработчик команды /news
@dp.message(Command("news"))
async def command_news_handler(message: Message) -> None:
    news = await get_news()
    if not news["status"]:
        await message.answer("ERROR: " + news["message"])
        return
    await message.answer(
        create_text_message(news["data"])
    )

# Обработчик всех остальных сообщений
@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text is None:
        return
    await message.answer(message.text)


# Главная функция для запуска бота
async def main() -> None:
    asyncio.create_task(scheduler())
    print("Bot started. Press Ctrl+C to stop.")
    await dp.start_polling(bot)

# Запуск главной функции при выполнении скрипта напрямую
if __name__ == "__main__":
    asyncio.run(main())