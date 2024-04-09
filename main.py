from BotManager import BotManager
from dotenv import load_dotenv
from tts.main import TTS
from os import getenv
import asyncio

load_dotenv()

#  Инициализация модели tts
tts_instance = TTS()

if __name__ == '__main__':
    bot = BotManager(getenv('TOKEN'))
    asyncio.run(bot.run())
