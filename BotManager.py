from aiogram import Bot, Dispatcher, types
from aiogram.executor import start_polling
from aiogram.contrib.middlewares.logging import LoggingMiddleware

class BotManager:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.dp.message.bind_filter(types.ChatTypeFilter(types.ChatType.PRIVATE))
        self.dp.message.middleware(LoggingMiddleware())

    async def on_start(self, message: types.Message):
        await message.answer("Привет! Я бот, который поможет тебе создать песню. Пожалуйста, выбери один из вариантов: текст, аудио, текст и аудио.")

    async def on_message(self, message: types.Message):
        # Здесь будет логика обработки сообщений
        await message.answer("Спасибо за твой выбор!")

    def setup(self):
        self.dp.message.register(self.on_start, commands=["start"])
        self.dp.message.register(self.on_message)

    def run(self):
        start_polling(self.dp, skip_updates=True)
