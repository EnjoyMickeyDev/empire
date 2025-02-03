import disnake
from disnake.ext import commands
from datetime import datetime
import re

from src.emoire import emoire

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot: emoire = bot

   
def setup(bot):
    bot.add_cog(Other(bot))