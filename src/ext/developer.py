import disnake
from disnake.ext import commands
from src.emoire import emoire

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot: emoire = bot

    @commands.slash_command(name='clear')
    @commands.has_permissions(administrator=True)
    async def clear(self, interaction: disnake.GuildCommandInteraction, count: int):
        """Удаляет указанное количество сообщений в канале."""
        if interaction.author.id != 627925818429145119:
            return await interaction.send("У вас нет прав для использования этой команды.", ephemeral=True)

        await interaction.channel.purge(limit=count + 1)  # Удаляем указанное количество сообщений + само сообщение с командой
        await interaction.send("Сообщения успешно удалены.", delete_after=5)

    @commands.slash_command(name='reboot')
    @commands.has_permissions(administrator=True)
    async def reboot(self, interaction: disnake.GuildCommandInteraction, extension: str = commands.Param(choices=['admin', 'other', 'developer', 'listeners'])):
        """Перезагружает указанное расширение."""
        try:
            self.bot.reload_extension(f'src.ext.{extension}')
            await interaction.send(f'Расширение `{extension}` успешно перезагружено.')
        except Exception as e:
            await interaction.send(f'Ошибка при перезагрузке расширения: {e}')

    @commands.slash_command(name='loaded')
    @commands.has_permissions(administrator=True)
    async def loaded(self, interaction: disnake.GuildCommandInteraction, extension: str):
        """Загружает указанное расширение."""
        try:
            self.bot.load_extension(f'src.ext.{extension}')
            await interaction.send(f'Расширение `{extension}` успешно загружено.')
        except Exception as e:
            await interaction.send(f'Ошибка при загрузке расширения: {e}')

def setup(bot):
    bot.add_cog(Developer(bot))