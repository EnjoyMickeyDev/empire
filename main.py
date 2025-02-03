import os

from dotenv import load_dotenv
from src.emoire import emoire

load_dotenv()

bot = emoire()
bot.load_extensions()

bot.run(os.getenv("TOKEN"))