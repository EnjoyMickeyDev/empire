import disnake
from disnake.ext import commands
from datetime import datetime
import re
from io import BytesIO
from src.emoire import emoire
from src.core.classes import PickOne
from src.core.enums import *
from src.core.time_util import *

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot: emoire = bot
    
    @commands.slash_command(name='post_up')
    @commands.has_permissions(administrator=True)
    async def post_up(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()

        embed = disnake.Embed(color=0x36393e)
        embed.set_image(url="https://media.discordapp.net/attachments/1333838836614299770/1333864254431826024/ima3ge.png?ex=679a7164&is=67991fe4&hm=73aaaf06c9c4f657632deba942d22de88f97d250ddb86f76bcd069485f53c8c8&=&format=webp&quality=lossless&width=1348&height=676")

        options = [
            disnake.SelectOption(label=f"{rank[0]} -> {rank[1]}", value=f"jn|{idx + 1}")
            for idx, rank in enumerate([
                ("Helper", "Junior Administrator"),
                ("Junior Administrator", "Administrator"),
                ("Administrator", "Senior Administrator")
            ])
        ]
        select = disnake.ui.Select(placeholder="Подать заявку", options=options)

        channel = interaction.guild.get_channel(1332438632442888337)
        await channel.send(embed=embed, components=[select])

        await interaction.send("Успешно отправлено.", ephemeral=True)

    @commands.slash_command(name='post_afk')
    @commands.has_permissions(administrator=True)
    async def post_afk(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()

        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="ㅤㅤㅤВзять отпускㅤㅤㅤ", custom_id="vacation"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="ㅤㅤㅤВзять отгул ㅤㅤㅤ", custom_id="time_off"))

        channel = interaction.guild.get_channel(1332438632744620151)
        await channel.send(view=view)

        await interaction.send("Успешно отправлено.", ephemeral=True)

    @commands.slash_command(name='post_shift')
    @commands.has_permissions(administrator=True)
    async def post_contract(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()

        embed = disnake.Embed(color=0x2F3136)
        embed.set_image(url="https://media.discordapp.net/attachments/1333838836614299770/1333864255988170772/ima1213123ge.png?ex=679a7164&is=67991fe4&hm=cd3ae191472112409c42819d062bd7876adad5bd3f2efa1117140bb9f82b6047&=&format=webp&quality=lossless&width=1348&height=676")

        view = PickOne(interaction.author.id)
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="ㅤㅤㅤНачать сменуㅤㅤㅤ", custom_id="start_shift"))
        view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.red, label="ㅤㅤㅤЗакончить сменуㅤㅤㅤ", custom_id="end_shift"))


        channel = interaction.guild.get_channel(1332438632744620149)
        await channel.send(embed=embed, view=view)

        await interaction.send("Успешно отправлено.", ephemeral=True)

    @commands.slash_command(name='post_tracker')
    @commands.has_permissions(administrator=True)
    async def post_tracker(self, interaction: disnake.GuildCommandInteraction):
        await interaction.response.defer()

        embed = disnake.Embed(color=0x2F3136)
        embed.set_image(url="https://media.discordapp.net/attachments/1333838836614299770/1333864313848336457/image.png")

        async def send_to_channel(channel_id, custom_id):
            channel = interaction.guild.get_channel(channel_id)
            if channel:
                view = PickOne(interaction.author.id)
                view.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, label="ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤПодать заявкуㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", custom_id=custom_id))
                await channel.send(embed=embed, view=view)

        await send_to_channel(1332438632744620145, "start_gos")
        await send_to_channel(1332438632744620146, "start_getto")
        await send_to_channel(1332438632744620147, "start_maffia")

        await interaction.send("Успешно отправлено.", ephemeral=True)
 

    @commands.slash_command(name='activity')
    @commands.has_permissions(administrator=True)
    async def activity(self, interaction: disnake.GuildCommandInteraction, member: disnake.Member):
        await interaction.response.defer()

        data = await self.bot.db.select_all(
            "*", 
            "member_shift", 
            where={
                "status": False,
                "member_id": member.id
            }
        )

        if not data:
            return await interaction.send(content="Рабочих смен не обнаружено.", ephemeral=True, delete_after=10)

        history = [
            f"• <t:{int(row['time_start'].timestamp())}:d> - Отработано: `{display_time(row['time_second'], full=True)}`"
            for row in data
        ]

        embed = disnake.Embed(
            color=0x00BFFF,
            description=(
                f"# **ИСТОРИЯ АКТИВНОСТИ**\n"
                f"Discord - {member.mention}\n"
                + "\n".join(history)
            )[:4000] 
        )

        await interaction.send(embed=embed, delete_after=60)
    

    @commands.slash_command(name='sql')
    @commands.has_permissions(administrator=True)
    async def sql(
        self, 
        interaction: disnake.GuildCommandInteraction, 
        query: str
    ):  
        try:
            resp = await self.bot.db.fetchrow(query)
            if not resp:
                resp = {}
        except Exception as e:
            return await interaction.send("Некорректный запрос.", ephemeral=True)

        embeds = []
        current_embed = disnake.Embed(description=query)

        for key, value in resp.items():
            value = f"'{value}'" if isinstance(value, str) else str(value)
            if len(current_embed.fields) == 25:
                embeds.append(current_embed)
                current_embed = disnake.Embed()
            current_embed.add_field(name=key, value=value, inline=True)

        if current_embed.fields:
            embeds.append(current_embed)

        await interaction.send(embeds=embeds[:10])  
    
    
def setup(bot):
    bot.add_cog(Admin(bot))