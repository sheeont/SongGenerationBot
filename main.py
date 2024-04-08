from BotManager import BotManager
from dotenv import load_dotenv
from os import getenv
import asyncio

load_dotenv()


if __name__ == '__main__':
    bot = BotManager(getenv('TOKEN'))
    asyncio.run(bot.run())
