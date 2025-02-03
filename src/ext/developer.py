import disnake
from disnake.ext import commands
from datetime import datetime
import re

from src.emoire import emoire
from src.core.classes import PickOne

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot: emoire = bot

    @commands.slash_command(name='clear')
    @commands.has_permissions(administrator=True)
    async def clear(
            self, 
            interaction: disnake.GuildCommandInteraction, 
            count: int, 
        ):
        if interaction.author.id == 627925818429145119:
            await interaction.channel.purge(limit=count + 1)
            await interaction.send("успешно", delete_after=5)
            
    @commands.slash_command(name='reboot')
    @commands.has_permissions(administrator=True)
    async def reboot(self, interaction: disnake.GuildCommandInteraction, extension: str = commands.Param(choices=['admin','other','developer', 'listeners', 'fun'])):
        try:
            self.bot.reload_extension(f'src.ext.{extension}')
            await interaction.send(f'Extension: `{extension}` успешно перезагружен.')
        except Exception as e:
            await interaction.send(f'Ошибка при перезагрузке кода: {e}')
    
    @commands.slash_command(name='loaded')
    @commands.has_permissions(administrator=True)
    async def loaded(self, interaction: disnake.GuildCommandInteraction, extension: str):
        try:
            self.bot.load_extension(f'src.ext.{extension}')
            await interaction.send(f'Extension: `{extension}` успешно загружен.')
        except Exception as e:
            await interaction.send(f'Ошибка при перезагрузке кода: {e}')

def setup(bot):
    bot.add_cog(Developer(bot))